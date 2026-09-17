# codebase/ — Prototype CP3 dùng AI thật

## Chạy thế nào

Yêu cầu Node.js 18 trở lên; không cần cài package ngoài.

```bash
cp .env.example .env
# Mở .env và điền OPENAI_API_KEY
npm start
```

Nếu server đang chạy khi bạn thêm key, nhấn `Ctrl+C` rồi chạy lại `npm start`.

Mở `http://127.0.0.1:4173`. Không mở `index.html` bằng `file://` khi demo CP3 vì trình duyệt cần gọi server cục bộ để giữ kín API key.

API key chỉ được đọc ở `codebase/server.mjs`, không được gửi xuống trình duyệt. File `.env` đã nằm trong `.gitignore`.

### Nguồn transcript nội bộ

Prototype chạy được ngay với `sources.example.json`, nhưng giao diện sẽ ghi rõ **NGUỒN MẪU**. Trước khi quay CP3:

```bash
cp codebase/prototype/sources.example.json codebase/prototype/sources.local.json
```

Thay bốn trường `text` trong `sources.local.json` bằng nội dung thật của `[T06-138]`, `[T06-141]`, `[T06-145]`, `[T06-149]`. File này được Git bỏ qua và không được đẩy lên repo public.

## Bốn màn

| Màn | Là gì |
|---|---|
| **M1 · Mở phiên** | Công bố trước phạm vi, tiêu chí "đã dạy được" và câu "đây không phải bài thi" — trước khi học viên gõ chữ nào |
| **M2 · Dạy lại** | Ô viết lời giải thích. Cột phải: 4 đoạn nguồn `[T06-xxx]` **luôn hiện** |
| **M3 · Agent hỏi ngược** | Chip trạng thái + mức tự tin + nội dung theo nhánh. Mỗi câu hỏi ngược gắn mã đoạn nó dựa vào |
| **M4 · Kết phiên** | Log phiên + kết luận theo đúng tiêu chí đã công bố ở M1 |

## Xem hệ thống đang làm gì

Nút **⤳ Sơ đồ luồng** ở góc phải thanh tiêu đề mở sơ đồ toàn bộ một vòng dạy lại: học viên nhập gì, hai cổng chặn trước, **điểm gọi quyết định AI** (`decide()`, viền tím đậm), ba nhánh đi ra, chặng correction và vòng lặp về M2. Bấm *← Quay lại bản mẫu* để về đúng màn đang dở.

Sơ đồ này cũng là hình thức nộp thứ hai mà mốc CP2 chấp nhận (flowchart), nằm luôn trong file bản mẫu nên không phải mở thêm gì.

## Bấm nút nào ra nhánh nào

Dùng **Bảng điều khiển demo** ở cuối màn M2 (4 nút preset) để demo 5 phút đi hết 4 nhánh mà không phụ thuộc gõ tay:

| Bấm | Nhánh | Trạng thái | Agent làm gì |
|---|---|---|---|
| ① Trả lời đủ ý | **happy path** | `ĐỦ_CĂN_CỨ` | Công nhận *tạm*, không tự chốt — đẩy học viên tự đối chiếu với đoạn nguồn |
| ② Trả lời thiếu ý | **low-confidence** | `THIẾU_CĂN_CỨ` | Hỏi ngược đúng 2 câu vào 2 tiêu chí còn hổng, không đưa đáp án |
| ③ Nói sang chuyện khác | **failure / no-grounding** | `NGOÀI_PHẠM_VI` | Nói thẳng là ngoài phạm vi, **không** phán đúng/sai |
| ④ Dán nguyên văn tài liệu | low-confidence *(hard test)* | `THIẾU_CĂN_CỨ` | Phát hiện dán lại tài liệu, đòi nói bằng lời mình |
| **Không đồng ý với đánh giá này** *(có ở mọi màn M3)* | **correction** | học viên chọn lại | Ghi phản hồi vào log; đánh giá của agent bị vô hiệu |

Gõ tự do sẽ gọi OpenAI Responses API qua server cục bộ. Hai trường hợp rẻ và rõ ràng — bài quá ngắn hoặc dán nguyên văn nguồn — được chặn trước để không tốn một lời gọi API.

## Phần nào thật, phần nào còn cần dữ liệu cục bộ

| Thành phần | Trạng thái CP3 |
|---|---|---|
| Luồng 4 màn, điều hướng, log phiên | **Thật**, chạy trong trình duyệt |
| Panel nguồn và correction | **Thật** |
| Quyết định ba trạng thái | **AI thật**, structured output từ Responses API |
| API key | **Server-side**, đọc từ `.env` |
| Bốn đoạn nguồn | Dùng `sources.local.json` nếu có; nếu chưa có thì dùng fixture và hiện cảnh báo |
| Hai cổng quá ngắn / dán nguyên văn | Kiểm tra cục bộ trước khi gọi AI |

## Chạy số đo CP3

Giữ server đang chạy, mở terminal thứ hai:

```bash
npm run eval
```

Script chạy 20 ca trong `eval/cases.json`, in `đúng/tổng` và lưu chi tiết vào `eval/results.json`. Chỉ quay con số thật được tạo sau lần chạy này.

## Sửa ở đâu

Các điểm chính:

| Muốn đổi | Sửa chỗ nào |
|---|---|
| Nội dung 4 đoạn nguồn thật | `prototype/sources.local.json` — không commit |
| Prompt, schema và model | `server.mjs` + `.env` |
| Câu trả lời mẫu cho demo | mảng `PRESET` |
| Gọi backend | hàm `decide()` trong `prototype/index.html` |
| Bộ 20 ca | `eval/cases.json` |
| Kịch bản quay | `evidence/cp3-video-script.md` |
