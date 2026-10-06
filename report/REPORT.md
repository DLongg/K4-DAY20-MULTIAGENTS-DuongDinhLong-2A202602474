# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Dương Đình Long | 2A202602474 | Toàn bộ bài lab |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `google_genai:gemini-3.5-flash-lite`, `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents==0.7.21`, Windows 11 (trực tiếp với Git toolchain trong PATH)
- Số lần chạy tác vụ đã dùng / ngân sách: 9 / 60
- Commit của tag `freeze`: `ff557d1`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Trên tập tác vụ đánh giá (eval), điều kiện subagents không cải thiện đáng kể điểm số so với baseline (chênh lệch điểm <= 0.05), trong khi lượng token tiêu thụ tăng gấp 2.5 - 3.5 lần. Căn cứ: kiến trúc đa tác tử phân tách ngữ cảnh (stateless subagents) chỉ hữu ích cho việc phân rã công việc kỹ thuật nhưng không thể tự suy luận ra các quy ước tổ chức ngầm (House Rules) chưa từng được nêu trong đề bài.
- H2 (skills-auto so với baseline): Trên tập tác vụ đánh giá (eval), điều kiện skills-auto có điểm số tương đương hoặc chỉ tăng rất nhẹ so với baseline, và thấp hơn đáng kể so với điểm tác vụ học (learn). Căn cứ: các skill do Curator sinh ra dựa trên phản hồi của tác vụ học có nguy cơ quá khớp (overfitting) vào các House Rules của tập học; khi chuyển sang tập đánh giá với các quy ước hoặc bài toán mới (out-of-distribution), các skill này không thể hỗ trợ trực tiếp.
- H3 (tác vụ học so với tác vụ đánh giá): Điều kiện skills-auto trên tác vụ học sẽ đạt điểm cao hơn rõ rệt (dự kiến tăng 15% - 30% nhờ giải quyết các check quy ước nhóm E đã ghi nhận), trong khi trên tác vụ đánh giá thì mức cải thiện gần như bằng 0 do quy ước đánh giá là hoàn toàn mới. Khoảng cách điểm giữa tác vụ học và tác vụ đánh giá sẽ phản ánh rõ mức độ tổng quát hóa/quá khớp của skill tự sinh.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: 7 công cụ tệp (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), 1 công cụ shell (`execute`), và 1 công cụ subagent (`task`). Công cụ duy nhất cho phép chạy lệnh shell trên hệ thống là `execute`.
2. Mô tả của công cụ `task` nêu rõ `general-purpose` là tác tử đa năng dùng để tra cứu thông tin phức tạp, tìm kiếm tệp và thực thi các tác vụ nhiều bước (có toàn quyền dùng các công cụ như tác tử chính). Subagent này có cơ chế cô lập ngữ cảnh (stateless): nó chỉ nhìn thấy nội dung văn bản cụ thể được truyền trong prompt của lệnh gọi `task`, không nhìn thấy lịch sử hội thoại trước đó của tác tử chính, và chỉ gửi lại một báo cáo tổng kết cuối cùng.
3. - Trích từ mô tả `task`: *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Trích từ mô tả `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `data-learn` | `rule_money_in_cents` | E | `"RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)."` |
| `data-learn` | `rule_meta_block` | E | `"RULE: answer.json has an object meta = {\"source\": <input file name>, ... rows_used: ...}."` |
| `data-learn` | `rule_clean_csv` | E | `"RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; ..."` |
| `code-learn` | `tests_not_modified` | B | `"the original files in tests/ must not be modified (new test files are allowed)"` |
| `code-learn` | `rule_type_hints` | E | `"RULE: every public function (name not starting with '_') in the package has type annotations..."` |
| `code-learn` | `rule_regression_tests` | E | `"RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3)..."` |
| `code-learn` | `rule_changelog` | E | `"RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet..."` |
| `logs-learn` | `rule_service_names` | E | `"RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service)."` |
| `logs-learn` | `rule_sorted_errors` | E | `"RULE: errors is sorted by service, then by timestamp_utc, ascending."` |
| `logs-learn` | `rule_schema_header` | E | `"RULE: the top-level object has 'schema_version': 2 and 'generated_by': 'log-triage'."` |

Nhận xét: 
- Nhóm lỗi chiếm đa số áp đảo là **Nhóm E (Vi phạm quy ước tổ chức - House Rules)**, chiếm 9/10 trường hợp thất bại. Điều này là do các quy ước này hoàn toàn không được mô tả tường minh trong `instruction.md` mà do bot đánh giá kiểm tra ngầm định.
- Về mặt kỹ thuật thuần túy (tính toán, xử lý múi giờ, phân tích log, sửa bug logic), mô hình đạt **17/18 check kỹ thuật** (bằng chứng phủ định cho các nhóm A, C, D).
- **Skill hoàn toàn có thể phòng ngừa triệt để Nhóm E**, vì Curator có thể trích xuất các quy tắc Acme này từ trường `detail` của bot đánh giá và hướng dẫn tác tử thực hiện đúng checklist ở các lần chạy sau.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):
  1. `explorer`: Đọc đề, khảo sát cấu trúc thư mục, log, code và tệp dữ liệu mà không chỉnh sửa tệp; giúp tác tử nắm rõ hiện trạng trước khi hành động.
  2. `implementer`: Trực tiếp thực hiện các chỉnh sửa, cài đặt tính năng, sửa bug, làm sạch dữ liệu và chạy test kiểm tra.
  3. `reviewer`: Rà soát độc lập các tệp đã sửa, kiểm tra lại các trường hợp biên và yêu cầu đề bài trước khi hoàn tất tác vụ.
- `subagent_calls` ở từng tác vụ và nhận xét:
  - `code-learn`: **8 lần gọi**. Tác tử chính giao việc liên tục cho subagent để kiểm tra bug, sửa đổi từng file và chạy test.
  - `data-learn`: **2 lần gọi**. Tác tử chính giao cho subagent khám phá dữ liệu ban đầu rồi tự hoàn tất các bước tính toán.
  - `logs-learn`: **0 lần gọi**. Do tác vụ đọc log và tạo file JSON tương đối tuyến tính và đơn giản, tác tử chính chọn giải quyết trực tiếp mà không cần phân rã cho subagent. Đây là hành vi hợp lý của LLM khi đánh giá chi phí ngữ cảnh.
- Thông tin thiếu hoặc thừa khi giao việc: Tác tử chính truyền tải khá đầy đủ các yêu cầu và đường dẫn trong prompt giao việc, tuy nhiên subagent không có ngữ cảnh quy ước ngầm nên các lỗi thuộc nhóm E vẫn không tự động được khắc phục.
- Ảnh hưởng đến token và thời gian:
  - `code-learn`: Token tăng từ 170,635 (`baseline`) lên 527,636 (`subagents`), gấp **~3.1 lần**. Thời gian tăng từ 128.5s lên 463.2s.
  - `data-learn`: Token tăng từ 247,549 (`baseline`) lên 647,437 (`subagents`), gấp **~2.6 lần**. Thời gian tăng từ 123.9s lên 368.4s.
  - `logs-learn`: Do `subagent_calls = 0`, token tăng nhẹ (53,139 lên 124,926) do phần system prompt bổ sung cho subagents.
  - Điểm số không có sự cải thiện đáng kể (code-learn 6/10 -> 6/10; data-learn 5/8 -> 4/8; logs-learn 6/9 -> 6/9) do subagents không có thêm thông tin về các quy ước tổ chức Acme. Đa tác tử làm tăng đáng kể chi phí token (2.5 - 3x) mà không cải thiện điểm quy ước ngầm.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: Chạy curator đúng 1 lần duy nhất (`python -m lab.curator`), số skill bị xóa: 0. Cả 3 skill được sinh ra đều vượt qua hàm kiểm định `validate_skill` ngay lần đầu (đầy đủ YAML frontmatter, độ dài hợp lệ, không chứa ký tự cấm `../`, không chứa tên tác vụ đánh giá).

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `canonical-data-cleaning-and-output-formatting` | Kết hợp: cấu trúc làm sạch dữ liệu tổng quát nhưng chứa quy ước ngầm riêng của Acme (`clean.csv`, khối `meta`, tiền tệ dạng integer cents). | Đúng theo logic kiểm tra của bot, nhưng diễn đạt mang tính điều kiện (*"When required by schema rules"*) nên tác tử chưa áp dụng định dạng cents khi đề không ghi rõ. | 9 dòng; `Use when processing datasets, cleaning CSVs, and generating JSON answers or summary metrics.`; `skills_read = 1` ở `data-learn`. |
| `log-parsing-and-normalization-rules` | Tổng quát cho việc bóc tách log và chuẩn hóa schema JSON Acme (thay '-' bằng '_' cho service, sort UTC, schema version). | Đúng hoàn toàn, phản ánh chính xác các quy tắc Acme trích xuất từ `detail` của bot chấm. | 9 dòng; `Use when parsing log files, extracting error entries, and formatting JSON outputs.`; `skills_read = 1` ở `logs-learn`. |
| `python-code-quality-and-testing-rules` | Tổng quát cho quy trình bảo trì gói Python (không sửa test gốc, thêm type hints, thêm regression test, cập nhật CHANGELOG). | Đúng hoàn toàn theo quy chuẩn Acme, giúp tác tử tự động bổ sung file test hồi quy `tests/test_regressions.py` và pass check. | 10 dòng; `Use when modifying Python packages, adding bug fixes, or writing tests.`; `skills_read = 1` ở `code-learn`. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
