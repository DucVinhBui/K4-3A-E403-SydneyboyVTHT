# Nhật ký khai phá dữ liệu — CP1

**Nguồn:** `data/vlearn-pack/chatlog/tutor_turns.csv` (không commit vào repo này theo quy định bảo mật — chỉ dẫn mã `turn_id`).
**Ngày chạy:** 16/09/2026 · **Người chạy:** _(điền tên)_

## 1. Phương pháp đếm (người khác chạy lại phải ra đúng số)

- Đọc bằng Python `csv.DictReader`. **Không dùng `awk -F,` hay `cut -d,`** — cột `student_question` và `tutor_reply` chứa dấu phẩy và ký tự xuống dòng bên trong dấu nháy kép, tách theo dấu phẩy sẽ ra số sai.
- Ba phạm vi báo cáo:
  - **ALL** = toàn bộ 13.494 lượt (22/07 → 15/09/2026)
  - **K4** = lọc `cohort_hint == "K4"` → 3.097 lượt (448 học viên, từ 09/09) — đây là khoá của nhóm
  - Khi nói về *"học viên tự hỏi gì"*: lọc thêm `is_preset == False` để loại câu mẫu bấm sẵn
- **Cảnh báo đã tính đến:** ngày 30/07 có 2.579 lượt (19,1% toàn bộ) do một hoạt động trên lớp, chi phối thống kê ALL. Vì nhóm kết luận trên phạm vi **K4** (từ 09/09) nên ngày này không nằm trong số liệu dùng để chọn bài toán.
- Quy tắc xếp loại: đếm trực tiếp giá trị cột, không suy diễn. `understanding_level` tính là "rỗng" khi chuỗi rỗng sau khi `.strip()`.

## 2. Số liệu

| Chỉ số | Cách đếm | ALL (n=13.494) | K4 (n=3.097) |
|---|---|---|---|
| Không ghi nhận mức hiểu | `understanding_level` rỗng | 13.474 (**99,85%**) | 3.091 (**99,81%**) |
| Có hỏi ngược lại người học | `move_used == "ask_probing_question"` | 28 (0,21%) | 6 (0,19%) |
| Giảng lại khái niệm | `move_used == "review_concept"` | 12.127 (89,9%) | 2.767 (89,3%) |
| Có phản hồi của người học | `rating` khác rỗng | 177 (1,31%) | 12 (0,39%) |
| Câu mẫu bấm sẵn | `is_preset == True` | 3.067 (22,7%) | 542 (17,5%) |
| Trả lời không trích dẫn | `has_citation == False` | 3.781 (28,0%) | 839 (27,1%) |
| Độ dài hỏi vs trả lời | TB `q_len` vs TB `reply_len` | 154,9 vs 1.051,6 (**6,8×**) | 158,3 vs 1.018,8 (**6,4×**) |

## 3. Đọc kỹ 6 lượt hỏi ngược của K4 (đọc nguyên văn từng lượt, không chỉ đếm)

6 lượt duy nhất được gắn `ask_probing_question` trong khoá K4:

| turn_id | Ngữ cảnh lượt hỏi | Phân loại |
|---|---|---|
| `T10507` | *"Hãy hỏi tôi những câu hỏi liên quan đến kiến thức…"* | học viên **tự đi xin** được hỏi |
| `T13177` | *"cho tôi câu hỏi về prompt engineering…"* | học viên **tự đi xin** được hỏi |
| `T10638` | *"repo không vào được"* | gỡ lỗi kỹ thuật, không phải kiểm tra hiểu |
| `T11458` | *"VẪn lỗi ạ"* | gỡ lỗi kỹ thuật, không phải kiểm tra hiểu |
| `T10300` | *"i've done it"* | hỏi ngược sau khi học viên báo xong việc |
| `T13197` | *"tôi ko hiểu câu quizz này"* | kiểm tra hiểu, nhưng **do học viên kêu trước** |

**Kết luận đếm được:** trong 3.097 lượt của khoá, số lượt hệ thống **chủ động** kiểm tra xem người học có thật sự hiểu hay không (khi người học không kêu và không tự đi xin) là **1 lượt — 0,03%**.

## 4. Năm ví dụ nguyên văn

*(trích tối đa 2 câu mỗi ví dụ theo quy định bảo mật, dẫn `turn_id` thay vì dán đoạn dài)*

| turn_id | Trích | Vì sao chọn |
|---|---|---|
| `T10296` | *"which model r u"* (15 ký tự) | học viên gõ cụt, không có gì để kiểm tra mức hiểu |
| `T10300` | *"i've done it"* | báo xong việc, không có bằng chứng nào về việc hiểu |
| `T10970` | hỏi *"RNN là gì"* (63 ký tự) → nhận lại 1.395 ký tự | tutor giảng một chiều, không câu hỏi ngược nào ở cuối |
| `T10939` | *"khác nhau như nào"* (67 ký tự, không nói rõ giữa gì) | hệ thống tự suy ngữ cảnh rồi giảng 1.573 ký tự |
| `T10507` | *"Hãy hỏi tôi những câu hỏi liên quan đến kiến thức…"* | học viên **phải tự đi xin** mới được hỏi ngược |

## 5. Lệnh chạy lại

```bash
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('data/vlearn-pack/chatlog/tutor_turns.csv',encoding='utf-8')))
k4=[r for r in rows if r['cohort_hint']=='K4']
n=len(k4)
ul=sum(1 for r in k4 if not r['understanding_level'].strip())
pr=sum(1 for r in k4 if r['move_used']=='ask_probing_question')
print(f"K4 n={n} | understanding_level rong={ul} ({ul/n*100:.2f}%) | probing={pr} ({pr/n*100:.2f}%)")
PY
```
