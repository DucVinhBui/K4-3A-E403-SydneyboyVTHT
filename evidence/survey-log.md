# Nhật ký khảo sát chuẩn A

**Khảo sát:** Cách mọi người học trong khoá AI20k  
**Nguồn:** [Google Form](https://docs.google.com/forms/d/14juAFGo64X_ekgWMhwQxPh24NBebLL7rNsDRf7BD9fw/edit?no_redirect=true#responses) · bộ câu hỏi tại [`survey-questions.md`](survey-questions.md)  
**Ngày trích dữ liệu:** 16/09/2026  
**Người phụ trách:** Đinh Công Tú — `2A202602479`  
**Mục tiêu chuẩn A:** ít nhất 20 người ngoài nhóm và hơn 50% số người thỏa định nghĩa xác nhận đã khóa trước khi phát form.

## 1. Phương pháp

- Đọc từng phiếu trong tab **Câu trả lời → Cá nhân** của Google Form, không suy ra câu trả lời cá nhân từ biểu đồ tổng hợp.
- Giữ nguyên văn C5 và C6, kể cả lỗi chính tả; câu không có nội dung được ghi là `*(bỏ trống)*`.
- Form có 6 lượt gửi. Lê Phan Việt Cường (`2A202602641`) gửi hai phiếu có nội dung trùng hoàn toàn lúc 19:24–19:25; giữ phiếu đầu và loại 1 phiếu trùng.
- Sau lọc trùng còn 5 người duy nhất. Khi tính chuẩn A, loại người thuộc nhóm theo danh sách trong [`../teammates.md`](../teammates.md):
  - Đinh Công Tú (`2A202602479`) chắc chắn là thành viên nhóm.
  - Phiếu “Đỗ Phúc Hưng” không có mã học viên và trùng tên thành viên nhóm Đỗ Phúc Hưng (`2A202602762`); để thận trọng, không tính phiếu này là người ngoài nhóm.
- Vì vậy, số người hợp lệ để đối chiếu ngưỡng **người ngoài nhóm** hiện tại là `n = 3`.

## 2. Định nghĩa xác nhận đã khóa trước khảo sát

Một người chỉ được tính là **xác nhận** khi thỏa đồng thời:

1. C2 chọn **“Thấy quen, đọc trôi được”** hoặc **“Đọc lại thấy ổn”** — điều kiện `(a)`.
2. C3 chọn **“Có — tôi kể lại được lần đó”** — điều kiện `(b)`.

Kết quả của từng người là `a ∧ b`. Không thay đổi định nghĩa sau khi xem dữ liệu.

## 3. Log nguyên văn theo từng người

| # | Họ tên | Mã học viên | Tư cách khi tính chuẩn A | C1 | C2 | C3 | C4 | Xác nhận `a∧b` | C5 — nguyên văn | C6 — nguyên văn |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Lê Phan Việt Cường | `2A202602641` | Ngoài nhóm | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — nhưng không nhớ rõ lần nào | Ngại hỏi / mất tự tin | Không | Học lec1 | *(bỏ trống)* |
| 2 | Đỗ Phúc Hưng | *(không cung cấp)* | Loại khỏi n ngoài nhóm: trùng tên thành viên nhóm, thiếu mã để xác minh | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — nhưng không nhớ rõ lần nào | Mất thời gian làm lại; Ngại hỏi / mất tự tin | Không | tôi học Transformet, hiểu khá sau | không |
| 3 | Đinh Công Tú | `2A202602479` | Thành viên nhóm — loại khỏi n ngoài nhóm | Hỏi AI tutor trên VLearn | Đọc lại thấy ổn | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz; Mất thời gian làm lại | Không | Khái niệm chung chung, đọc lại không hiểu sâu | Có cần người huongws dẫn, kiểm tra lại |
| 4 | Bùi Gia Chính | `2A202602693` | Ngoài nhóm | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz | Không | Khi học về các nội dung buổi 1, 2, tôi trả lời sai khái niệm ở quiz ôn tập | *(bỏ trống)* |
| 5 | Nguyễn Ngọc Thái An | `2A202602462` | Ngoài nhóm | Đọc lại slide một lượt nữa | Đọc lại thấy ổn | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz | Không | Phát hiện nhớ nhầm về attention trong transformer<br>Phát hiện ra lúc search lại trên mạng | *(bỏ trống)* |

## 4. Kiểm tra phiếu trùng

Phiếu bị loại là lượt gửi thứ hai của **Lê Phan Việt Cường — `2A202602641`**. Nội dung C1–C6 trùng hoàn toàn với dòng 1:

- C1: Hỏi AI tutor trên VLearn
- C2: Tự làm được bài tập về nó
- C3: Có — nhưng không nhớ rõ lần nào
- C4: Ngại hỏi / mất tự tin
- C5: Học lec1
- C6: *(bỏ trống)*

Phiếu này chỉ được ghi để kiểm toán số lượt gửi, không tham gia bất kỳ phép đếm nào.

## 5. Tổng kết theo đúng ngưỡng chuẩn A

### Kết quả chính

- Lượt gửi thô: **6**
- Phiếu trùng bị loại: **1**
- Người duy nhất sau lọc trùng: **5**
- Người hợp lệ ngoài nhóm: **3**
- Số người ngoài nhóm thỏa `(a)`: **2/3** — Bùi Gia Chính và Nguyễn Ngọc Thái An
- Số người ngoài nhóm thỏa `(b)`: **0/3**
- Số xác nhận `a ∧ b`: **0/3**
- **Tỉ lệ xác nhận: 0%**
- **Kết luận: chưa đạt chuẩn A** — chưa đủ `n ≥ 20` và tỉ lệ không lớn hơn 50%.

### Phân bố trong 3 phiếu ngoài nhóm hợp lệ

- C1: mỗi phương án *“Hỏi AI tutor trên VLearn”*, *“Đi thẳng sang phần tiếp theo”* và *“Đọc lại slide một lượt nữa”* có 1/3.
- C2: *“Thấy quen, đọc trôi được”* có 1/3; *“Đọc lại thấy ổn”* có 1/3; *“Tự làm được bài tập về nó”* có 1/3.
- C3: cả 3/3 chọn *“Có — nhưng không nhớ rõ lần nào”*; không ai chọn *“Có — tôi kể lại được lần đó”*.
- C4: *“Mất điểm bài tập/quiz”* nhiều nhất với 2/3; *“Ngại hỏi / mất tự tin”* có 1/3.

### Điều dữ liệu hiện tại nói được và chưa nói được

Dữ liệu hiện tại cho thấy cả ba người ngoài nhóm đều nói đã từng phát hiện mình hiểu sai, nhưng không ai nhớ rõ một tình huống đủ cụ thể để thỏa điều kiện `(b)`. Hai người báo hậu quả là mất điểm quiz. Đây là tín hiệu để tiếp tục hỏi sâu về các lần làm quiz sai, nhưng **chưa phải bằng chứng xác nhận nỗi đau** theo định nghĩa đã khóa.

Không được dùng 0/5 hoặc 0/6 làm tỉ lệ chuẩn A: mẫu chuẩn A chỉ tính người ngoài nhóm, sau lọc trùng. Cần thu thêm ít nhất **17 người ngoài nhóm hợp lệ** để đạt cỡ mẫu tối thiểu 20; nên thu dư để bù phiếu trùng, thiếu mã hoặc người thuộc nhóm.

## 6. Năm câu C5 nguyên văn để chuyển cho `spec.md` §1

> “Học lec1”  
> — Lê Phan Việt Cường

> “tôi học Transformet, hiểu khá sau”  
> — Đỗ Phúc Hưng *(không tính vào n ngoài nhóm)*

> “Khái niệm chung chung, đọc lại không hiểu sâu”  
> — Đinh Công Tú *(thành viên nhóm; không tính vào n ngoài nhóm)*

> “Khi học về các nội dung buổi 1, 2, tôi trả lời sai khái niệm ở quiz ôn tập”  
> — Bùi Gia Chính

> “Phát hiện nhớ nhầm về attention trong transformer  
> Phát hiện ra lúc search lại trên mạng”  
> — Nguyễn Ngọc Thái An

> **Lưu ý khi cập nhật `spec.md`:** chỉ có 3 quote đến từ người ngoài nhóm đã xác minh. Cần lấy thêm ít nhất 2 quote nguyên văn từ người ngoài nhóm trước khi dùng bộ 5 quote làm bằng chứng chuẩn A.

## 7. Việc cần làm tiếp

1. Tiếp tục thu tối thiểu 17 người ngoài nhóm hợp lệ; mục tiêu thực tế nên cao hơn 17 để dự phòng dữ liệu không hợp lệ.
2. Yêu cầu người trả lời nhập đủ **họ tên + mã học viên**; kiểm tra ngay sau khi họ gửi.
3. Không mời thành viên nhóm điền form dùng để tính chuẩn A.
4. Với người chọn C3 *“Có — nhưng không nhớ rõ lần nào”*, phỏng vấn gợi nhớ bằng mốc quiz, bài học hoặc lần phải làm lại; vẫn giữ câu trả lời form ban đầu, không sửa hồi tố.
5. Khi có dữ liệu mới, lọc trùng theo mã học viên, cập nhật bảng và tính lại `n · số xác nhận · tỉ lệ %` theo đúng định nghĩa ở §2.
