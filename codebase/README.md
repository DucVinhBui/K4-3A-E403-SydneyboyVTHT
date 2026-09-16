# codebase/ — Bản mẫu tương tác CP2

## Mở thế nào

Tải repo về → double-click **`codebase/prototype/index.html`**.

Một file HTML duy nhất, tự chứa hoàn toàn: không framework, không CDN, không cài gì, **không cần mạng**. Mở bằng `file://` chạy được.

## Bốn màn

| Màn | Là gì |
|---|---|
| **M1 · Mở phiên** | Công bố trước phạm vi, tiêu chí "đã dạy được" và câu "đây không phải bài thi" — trước khi học viên gõ chữ nào |
| **M2 · Dạy lại** | Ô viết lời giải thích. Cột phải: 4 đoạn nguồn `[T06-xxx]` **luôn hiện** |
| **M3 · Agent hỏi ngược** | Chip trạng thái + mức tự tin + nội dung theo nhánh. Mỗi câu hỏi ngược gắn mã đoạn nó dựa vào |
| **M4 · Kết phiên** | Log phiên + kết luận theo đúng tiêu chí đã công bố ở M1 |

## Bấm nút nào ra nhánh nào

Dùng **Bảng điều khiển demo** ở cuối màn M2 (4 nút preset) để demo 5 phút đi hết 4 nhánh mà không phụ thuộc gõ tay:

| Bấm | Nhánh | Trạng thái | Agent làm gì |
|---|---|---|---|
| ① Trả lời đủ ý | **happy path** | `ĐỦ_CĂN_CỨ` | Công nhận *tạm*, không tự chốt — đẩy học viên tự đối chiếu với đoạn nguồn |
| ② Trả lời thiếu ý | **low-confidence** | `THIẾU_CĂN_CỨ` | Hỏi ngược đúng 2 câu vào 2 tiêu chí còn hổng, không đưa đáp án |
| ③ Nói sang chuyện khác | **failure / no-grounding** | `NGOÀI_PHẠM_VI` | Nói thẳng là ngoài phạm vi, **không** phán đúng/sai |
| ④ Dán nguyên văn tài liệu | low-confidence *(hard test)* | `THIẾU_CĂN_CỨ` | Phát hiện dán lại tài liệu, đòi nói bằng lời mình |
| **Không đồng ý với đánh giá này** *(có ở mọi màn M3)* | **correction** | học viên chọn lại | Ghi phản hồi vào log; đánh giá của agent bị vô hiệu |

Gõ tự do cũng chạy — quyết định đi qua một bộ định tuyến heuristic.

## Phần nào mock, phần nào thật

| | CP2 (bản này) | CP3 làm gì tiếp |
|---|---|---|
| Luồng 4 màn, điều hướng, log phiên | **thật** | giữ nguyên |
| Panel đoạn nguồn luôn hiện, nút correction | **thật** | giữ nguyên |
| **Quyết định chọn trạng thái** | **mock** — heuristic đếm từ khoá trong `decide()` | thay bằng lời gọi AI thật |
| **Nội dung 4 đoạn `[T06-xxx]`** | **mock** — fixture nhóm tự viết | đọc thẳng từ `transcript-06-clean.md` |
| Tiêu chí "đã dạy được" | **mock** — ngưỡng cứng 3/3 tiêu chí | LLM-judge (transcript là văn nói, so chuỗi sẽ vỡ — xem `spec.md` §5) |

> ⚠️ **Vì sao đoạn nguồn là fixture tự viết:** data pack của khoá là tài liệu nội bộ và repo này đang public, nên không đưa nội dung transcript thật vào đây. Mọi fixture đều gắn nhãn `MOCK` ngay trên giao diện.

## Sửa ở đâu

Toàn bộ trong `prototype/index.html`:

| Muốn đổi | Sửa chỗ nào |
|---|---|
| Nội dung 4 đoạn nguồn | mảng `SRC` |
| 3 tiêu chí "đã dạy được" + câu hỏi ngược | mảng `CRIT` |
| Câu trả lời mẫu cho demo | mảng `PRESET` |
| **Logic quyết định** | hàm `decide()` — đây là chỗ CP3 cắm lời gọi AI vào |
