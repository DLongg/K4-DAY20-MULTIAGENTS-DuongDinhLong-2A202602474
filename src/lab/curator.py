"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import json
import re
from pathlib import Path

from .model import make_model
from .tasks import ROOT, eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    out_path = Path(out_dir) if out_dir is not None else (ROOT / "skills" / "auto")

    runs = []
    base_dir = Path(results_dir) / source_condition
    if base_dir.exists():
        for run_file in sorted(base_dir.glob("*/run.json")):
            try:
                r = json.loads(run_file.read_text(encoding="utf-8"))
            except Exception:
                continue

            if r.get("role") != "learn":
                continue

            failed = [
                (c.get("name", ""), c.get("detail", ""))
                for c in r.get("checks", [])
                if not c.get("passed")
            ]
            if not failed:
                continue

            trace_file = run_file.parent / "trace.md"
            trace_tail = ""
            if trace_file.exists():
                trace_content = trace_file.read_text(encoding="utf-8")
                trace_tail = trace_content[-6000:]

            runs.append({
                "task": r.get("task", run_file.parent.name),
                "failed": failed,
                "trace": trace_tail,
            })

    if not runs:
        print("Warning: no failed checks found in learning tasks")
        return []

    sections = []
    for r in runs:
        failed_lines = "\n".join(f"- Check: {name}\n  Feedback: {detail}" for name, detail in r["failed"])
        sec = f"### Task: {r['task']}\nFailed checks:\n{failed_lines}\n"
        if r["trace"]:
            sec += f"\nTrace excerpt (end of run):\n```\n{r['trace']}\n```\n"
        sections.append(sec)

    prompt = (
        f"You are curating operational SKILLs for engineering and data analysis agents.\n"
        f"Below are the failed checks (check names and reviewer bot feedback) and execution traces from previous runs on LEARNING tasks.\n"
        f"Identify common procedural errors and organizational rules (not specific answers) and write up to {max_skills} short skills "
        f"that help avoid these failures on NEW tasks of the same type.\n\n"
        f"Rules:\n"
        f"- The skill must be general: do NOT mention specific task ids, specific test file names, exact answers, or hardcoded numbers.\n"
        f"- Each skill must have YAML frontmatter with 'name' (lowercase letters, numbers, and hyphens ONLY, e.g. acme-code-rules; never use underscores) and 'description' (one sentence stating WHEN TO USE).\n"
        f"- The body should be an actionable checklist or imperative steps (at most 40 lines).\n"
        f"- Output format for each skill, exactly:\n"
        f"=== SKILL: <name> ===\n"
        f"---\n"
        f"name: <name>\n"
        f"description: Use when ...\n"
        f"---\n"
        f"# <Title>\n\n"
        f"<actionable instructions>\n"
        f"=== END ===\n\n"
        + "\n\n".join(sections)
    )

    m = model or make_model()
    res = m.invoke(prompt)
    raw = res.content
    if isinstance(raw, str):
        reply = raw
    elif isinstance(raw, list):
        parts = []
        for p in raw:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict) and "text" in p:
                parts.append(p["text"])
        reply = "".join(parts)
    else:
        reply = str(raw)

    written = []
    for name, text in parse_skill_blocks(reply):
        if len(written) >= max_skills:
            break
        # Normalize underscores to hyphens if any
        clean_name = name.replace("_", "-")
        if clean_name != name:
            text = re.sub(r"^name:\s*" + re.escape(name), f"name: {clean_name}", text, flags=re.M)
            name = clean_name
        if validate_skill(text, expected_name=name):
            continue
        skill_dir = out_path / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        file_path = skill_dir / "SKILL.md"
        file_path.write_text(text, encoding="utf-8")
        written.append(file_path)

    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
