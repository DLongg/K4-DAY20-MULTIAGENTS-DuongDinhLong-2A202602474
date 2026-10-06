"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Use to inspect the workspace, examine files, read instructions, documentation, logs, or code, and report findings without modifying any files.",
            "system_prompt": "You are a code and data explorer. Your role is to explore files, inspect structure, and summarize facts accurately. Never edit or create files.",
        },
        {
            "name": "implementer",
            "description": "Use to implement changes, fix bugs in code, clean data files, or produce requested output files according to instructions.",
            "system_prompt": "You are an implementer. Your role is to execute changes, modify files, write output files, and run tests or scripts to verify your changes.",
        },
        {
            "name": "reviewer",
            "description": "Use to independently review work, verify changes against all rules and specifications, and check edge cases before declaring completion.",
            "system_prompt": "You are a reviewer. Your role is to verify all outputs and code changes against the specifications, run tests, and report whether all criteria are met.",
        },
    ]
