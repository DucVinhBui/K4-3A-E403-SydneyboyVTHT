# `knowledge/` — knowledge base của agent học trò

Đây là **nguồn sự thật duy nhất** mà agent được phép đối chiếu. Không có đoạn
nào trong này thì agent không có căn cứ, và phải trả `NGOÀI_PHẠM_VI` chứ không
được tự suy ra.

## Các pack hiện có

| file | khái niệm | mã đoạn |
|---|---|---|
| `hallucination.json` | vì sao LLM bịa *(mặc định)* | `[T06-138]`–`[T06-149]` |
| `toolcall.json` | vì sao phải cho LLM gọi công cụ | `[KB-TOOL-01]`–`[KB-TOOL-04]` |
| `grounding.json` | vì sao phải cấp nguồn cho mô hình đọc | `[KB-RAG-01]`–`[KB-RAG-04]` |
| `eval-first.json` | vì sao phải có bộ đo trước khi chỉnh prompt | `[KB-EVAL-01]`–`[KB-EVAL-04]` |
| `automation-level.json` | chọn mức tự động theo chi phí sai | `[KB-AUTO-01]`–`[KB-AUTO-04]` |

Chọn pack bằng biến môi trường, mặc định là `hallucination`:

```bash
cd codebase
MINILAB_TOPIC=grounding ../.venv/bin/python -m api.server --port 8765
```

Bản mẫu HTML tự nạp pack đang chạy qua `GET /api/scope`, nên cột đoạn nguồn,
ba tiêu chí ở màn M1 và câu hỏi ở màn M2 luôn khớp với thứ agent thật sự chấm.

## Nguồn gốc nội dung — đọc trước khi trích dẫn số đo

Toàn bộ 5 pack hiện tại là **MOCK do nhóm tự viết**, trường `source_label` của
từng file ghi rõ. Data pack của khoá là tài liệu nội bộ và repo nộp bài đang
public, nên nhóm không đưa transcript thật vào file commit (xem `spec.md` §4 và
`README.md` gốc, mục bảo mật dữ liệu).

Mã `T06-xxx` trong `hallucination.json` là **mã giả bắt chước cách đánh số** của
data pack, không trỏ tới lượt thoại thật nào. Các pack còn lại dùng tiền tố
`KB-` để không ai nhầm chúng với mã transcript của khoá.

Khi có data pack thật: thay nội dung `excerpts` bằng đoạn trích thật, sửa
`source_label`, rồi **chạy lại cả hai bộ đo** — số cũ không còn mô tả đúng hệ
thống nữa.

## Thêm một pack mới

Tạo `knowledge/<tên>.json`, tên file phải trùng trường `name`:

```json
{
  "name": "ten-pack",
  "title": "Tiêu đề ngắn",
  "concept": "khái niệm học viên phải dạy lại",
  "domain": "AI và cách làm sản phẩm AI",
  "persona_gap": "chỗ agent đang hổng — hiện ở màn M1",
  "scope_range": "[KB-XXX-01]–[KB-XXX-04]",
  "source_label": "MOCK — nhóm tự viết",
  "out_of_scope_examples": ["khái niệm AI khác, gọi tên được"],
  "excerpts": [{"id": "KB-XXX-01", "text": "..."}],
  "criteria": [{"key": "c1", "src": "KB-XXX-01", "label": "...", "probe": "..."}],
  "deep_probe": {"src": "KB-XXX-04", "text": "..."}
}
```

Ràng buộc bị kiểm lúc nạp, sai là **nổ ngay khi khởi động** chứ không chạy tiếp
với knowledge base hỏng: mã đoạn không được trùng; mọi `criteria[].src` và
`deep_probe.src` phải là mã CÓ THẬT trong `excerpts`; `name` phải trùng tên file.

Thêm pack xong nhớ thêm ca vào `eval/kb_cases.json` rồi chạy bộ kiểm chứng.

## Kiểm chứng

```bash
cd codebase
../.venv/bin/python -m eval.run_kb_check --structure-only   # không tốn tiền API
../.venv/bin/python -m eval.run_kb_check                    # gọi AI thật
```

Tầng A kiểm cấu trúc mọi pack. Tầng B chạy `eval/kb_cases.json` với **từng**
pack và kiểm hai thứ: state có đúng không, và mọi mã đoạn agent trích ra có
thật sự nằm trong pack không (chốt chống bịa mã). Kết quả ghi vào
`eval/kb_check_results.json`.

Ca `shared` chạy với mọi pack và là chỗ chốt một yêu cầu quan trọng: bài lạc
lĩnh vực (`"mỳ cay"`, `"asdkjfh qwe"`) phải ra `NGOÀI_PHẠM_VI` **kể cả khi rất
ngắn** — không được rơi vào `THIẾU_CĂN_CỨ` chỉ vì đếm số ký tự.
