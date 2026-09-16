# AI SPEC — Agent học trò: học bằng cách dạy lại · Nhóm SydleyboyVTHT · Lớp 3A · Phòng E403

**Track:** D — Học tập thích ứng & tương tác trên VLearn · **Đề:** D3 — Học bằng cách dạy
**Loại:** Tính năng mới
**Trạng thái:** bản CP1 (Canvas 4 ô) — hoàn thiện đến hạn chốt spec 21:00 ngày 17/9 (CP4)

---

## §1. User & Job

### Job executor
Học viên khoá 4 vừa học xong một khái niệm trong bài Foundation (transformer & attention) trên VLearn.

### Quy trình hiện tại (chưa có sản phẩm của nhóm)
Nghe giảng / đọc slide → thấy chưa chắc thì bôi đen đoạn và hỏi tutor → nhận về một đoạn giảng trung bình **1.019 ký tự** (dài gấp **6,4×** câu hỏi của chính mình) → tự kết luận "chắc là hiểu rồi" → đi tiếp sang phần sau.

### Core JTBD *(không có tên sản phẩm / không có chữ AI)*
> Xác nhận mình đã thật sự hiểu một khái niệm vừa học, trước khi đi tiếp.

*Tự kiểm: bỏ AI đi, việc này còn tồn tại không? — Còn. Học viên vẫn cần biết mình hiểu hay chưa, bằng cách hỏi bạn, tự làm bài, hoặc giải thích lại cho người khác.*

### Problem statement *(một câu, KHÔNG chữ AI)*
> Học viên K4 rời một bài học với cảm giác đã hiểu mà không có bằng chứng nào cho thấy lời giải thích của chính họ đúng hay sai: trong 3.097 lượt hỏi-đáp của khoá, 99,81% lượt không ghi nhận mức hiểu nào, và chỉ 1 lượt duy nhất (0,03%) là có ai đó chủ động hỏi ngược lại người học để kiểm tra.

### Evidence — chuẩn B (mining), đang bổ sung chuẩn A (khảo sát)

Log đầy đủ + phương pháp đếm kiểm lại được: **[`evidence/mining-log.md`](evidence/mining-log.md)**

| Số liệu | ALL (n=13.494) | K4 (n=3.097) |
|---|---|---|
| Không ghi nhận mức hiểu (`understanding_level` rỗng) | 99,85% | **99,81%** |
| Có hỏi ngược người học (`ask_probing_question`) | 28 (0,21%) | 6 (0,19%) |
| **Chủ động** kiểm tra hiểu (đọc nguyên văn 6 lượt K4) | — | **1 lượt (0,03%)** |
| Có phản hồi của người học (`rating`) | 1,31% | 0,39% |
| Độ dài trả lời / câu hỏi | 6,8× | **6,4×** |

Năm ví dụ nguyên văn kèm `turn_id`: `T10296` · `T10300` · `T10970` · `T10939` · `T10507` — xem `evidence/mining-log.md` §4.

#### Chuẩn A — đang chạy, chốt trước CP4

Bộ câu hỏi: **[`evidence/survey-questions.md`](evidence/survey-questions.md)** · Log kết quả: `evidence/survey-log.md` *(đang thu)*

**Định nghĩa "một người xác nhận" — chốt trước khi phát form, không sửa sau:** người trả lời thoả CẢ HAI: **(a)** ở Câu 2 chọn *"Thấy quen, đọc trôi được"* hoặc *"Đọc lại thấy ổn"* (căn cứ duy nhất là cảm giác, không có bằng chứng bên ngoài), **VÀ (b)** ở Câu 3 chọn *"Có — và tôi kể lại được lần đó"* (đã thật sự hiểu sai sau khi tưởng đã hiểu).

**Ngưỡng đạt:** n ≥ 20 người ngoài nhóm và tỉ lệ xác nhận > 50%.

**Bộ câu hỏi có thể fail:** người chọn *"Tự làm được bài tập"* hoặc *"Giải thích lại được cho người khác"* ở C5 là người **không** xác nhận. Nếu >50% chọn nhóm đó thì nỗi đau nhóm giả định không tồn tại và nhóm chọn lại bài toán — ghi vào §9 Changelog.

| | n | Xác nhận | Tỉ lệ | Đạt? |
|---|---|---|---|---|
| Kết quả | ___ | ___ | ___% | ___ |

---

## §2. Impact & quyết định chọn

### Bảng impact — 3 ứng viên trong track D *(số liệu riêng khoá K4, n = 3.097 lượt)*

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Build nổi trong 47,5h? | Chọn? |
|---|---|---|---|---|---|
| **D1** · Lớp học mô phỏng đa tác tử | 38,0% phiên học dừng sau đúng 1 lượt (301/792 phiên) | mỗi lần vào học | đọc một khối giảng dài gấp 6,4× câu hỏi rồi thoát, không ai phản biện | **Mock** — điều phối lượt là chỗ dễ vỡ nhất, mà rubric riêng của đề cho đúng 15 điểm cho phần đó | Loại |
| **D2** · Làm bài trước, giảng sau | 62,9% cặp học-viên×bài phải hỏi ≥2 lượt (417/663); 42,1% cần ≥3 lượt | mỗi bài tập | 94,3% lượt chỉ được giảng lại từ đầu, chỉ 1,29% là gợi ý/chẩn đoán riêng | **Mock** — 6 transcript không đủ để ra đề, phải tự soạn bài tập + ngân hàng 15–20 lỗi thường gặp trước khi chạy được lượt demo đầu | Loại |
| **D3** · Học bằng cách dạy lại | **99,81%** lượt không ghi nhận mức hiểu; chỉ **1 lượt (0,03%)** chủ động kiểm tra hiểu | mỗi khái niệm học xong | rời bài học với cảm giác đã hiểu, không có gì kiểm chứng lời giải thích của chính mình | **Working thu hẹp** — nguồn đối chiếu có sẵn: `transcript-06` có 162 mã `[T06-NNN]`, 2 đoạn dùng được ngay làm chuẩn | **CHỌN** |

### Ứng viên đã loại + lý do

- **D1 bị loại** vì chi phí cao nhất mà chỉ đạt tới Mock: phần khó nhất là điều phối lượt (ai nói khi nào, khi nào im để học viên tự nghĩ), và đó cũng chính là ô 15 điểm trong rubric riêng của đề. Nhóm không đủ giờ để làm tới nơi.
- **D2 bị loại** vì phải dựng hai thứ trước khi có lượt demo đầu tiên: bộ bài tập "trước khi học" và ngân hàng lỗi thường gặp. 6 transcript trong pack là bản gỡ băng lời giảng, không phải ngân hàng bài tập — chỉ transcript-03 và phần quiz trong transcript-04 tái dùng được.

### Ứng viên được chọn + lý do bằng số

**D3**, vì ba lý do:
1. **Bằng chứng mạnh nhất và sạch nhất** — 99,81% và 0,03% là hai con số đếm trực tiếp trên cột, không qua suy diễn, ai chạy lại cũng ra đúng.
2. **Là ứng viên duy nhất đạt được mức Working** trong 47,5 giờ. D1 và D2 đều dừng ở Mock.
3. **Nguồn đối chiếu đã có sẵn, không phải dựng**: `transcript-06-clean.md` có 162 mã đoạn để trích dẫn, trong đó self-attention `[T06-130]`–`[T06-132]` và hallucination `[T06-138]`–`[T06-149]` dùng được ngay làm chuẩn để chấm lời giải thích của học viên.

---

## §4. Thiết kế

### Lát cắt MỘT CÂU
> Một học viên K4 vừa học xong đoạn "vì sao LLM bịa" **cần** giải thích lại khái niệm đó bằng lời của mình, **được** một agent học trò đối chiếu lời giải thích với đoạn `[T06-138]`–`[T06-149]` và quyết định hỏi ngược đúng 2 câu tại chỗ thiếu căn cứ, **giúp** học viên bổ sung được dẫn chứng còn thiếu và đạt mức "đã dạy được" theo tiêu chí công bố trước phiên.

### Non-goals — những thứ KHÔNG build
1. **Không chấm điểm học viên.** Đây là chỗ luyện, không phải chỗ thi — không có điểm số nào được ghi lại hay báo về giảng viên dưới dạng đánh giá.
2. **Chỉ một bài giảng** (`transcript-06`) và **một khái niệm** ("vì sao LLM bịa"). Không đa bài, không đa khái niệm.
3. **Không có persona thay đổi theo lịch sử học viên.** Agent học trò có một mức hiểu cố định, công bố trước.
4. **Không đa tác tử.** Đúng một vai agent.

### Mức prototype nhắm tới
**Working (thu hẹp phạm vi)** — agent gọi thật, đối chiếu thật với đoạn transcript có mã.
- *Thật:* lời gọi AI ở quyết định trung tâm (chọn chỗ hổng để hỏi ngược), truy xuất đoạn `[T06-xxx]`, giao diện phiên dạy
- *Mock:* tiêu chí "đã dạy được" ở bản đầu dùng ngưỡng cứng; log phiên cho giảng viên chỉ là bảng

### Automation: **augment**
Lý do theo cost-of-error: quyết định đắt nhất **không phải** "hỏi ngược sai chỗ" — học viên thấy câu hỏi lạc thì bỏ qua được, sửa rẻ. Đắt nhất là agent **công nhận "đã hiểu" cho một lời giải thích sai**: học viên rời đi với kiến thức sai và **không tự phát hiện được**, sai lan sang các bài sau. Nên agent không tự chốt: đoạn `[T06-xxx]` gốc luôn hiển thị cạnh câu hỏi để học viên tự đối chiếu, và học viên luôn xem được mình bị đánh giá thiếu ở đâu.

### §4b. Nguyên tắc đã áp dụng
*(≥4 nguyên tắc, mỗi cái trỏ vào một chỗ cụ thể — hoàn thiện trước CP4)*

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G10** — Thu hẹp phạm vi khi nghi ngờ *(bắt buộc)* | Khi lời giải thích của học viên nằm ngoài đoạn `[T06-138]`–`[T06-149]`, agent nói rõ "phần này không có trong đoạn đang học" thay vì tự phán đúng/sai |
| **G11** — Giải thích vì sao | Mỗi câu hỏi ngược hiện kèm mã đoạn `[T06-xxx]` mà nó dựa vào |
| **G2** — Làm rõ nó làm tốt đến đâu | Màn hình mở đầu công bố trước tiêu chí "đã dạy được" và phạm vi: chỉ đối chiếu với transcript buổi Foundation |
| **G9** — Sửa dễ dàng | Học viên bổ sung/viết lại lời giải thích ngay trên cùng màn hình, không phải bắt đầu lại phiên |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản
*(≥8 kịch bản — hoàn thiện trước CP4)*

Rủi ro lớn nhất đã xác định: transcript là **văn nói** (ẩn dụ, ngắt câu tự nhiên), nên so khớp lời giải thích bằng keyword/regex sẽ vỡ ngay ở trường hợp *"học viên giải thích đúng nhưng khác cách diễn đạt tài liệu"*. Phải đối chiếu ngữ nghĩa, không phải so chuỗi.

| Lớp | Tình huống | Hành vi mong muốn |
|---|---|---|
| ① Nguồn sự thật | Học viên nói một ý đúng nhưng không có trong transcript-06 | Nói rõ "ngoài phạm vi đoạn đang học", không phán đúng/sai |
| ② Mơ hồ | Học viên chỉ gõ 1 dòng ngắn, không đủ để đánh giá | Hỏi lại một câu để lấy thêm, không kết luận |
| ③ Ngoài phạm vi | Học viên đòi "cho tôi đáp án luôn" | Từ chối đưa đáp án, đưa lại đoạn nguồn để tự đọc |
| ④ Đặc thù domain | Học viên giải thích **sai nhưng rất tự tin** | Không công nhận "đã hiểu"; hỏi ngược đúng chỗ sai, kèm mã đoạn |

*(còn ≥4 kịch bản nữa — bổ sung trước CP4)*

---

## §6. Bốn đường đi của trải nghiệm
*(hoàn thiện trước CP4)*

---

## §7. Kiểm thử
*(hoàn thiện trước CP4 — quality bar chốt tại 21:00 17/9 và giữ nguyên sau đó)*

**Ràng buộc riêng của track D:** quality bar bắt buộc có ít nhất một chỉ số về **việc học**, không chỉ "AI trả lời đúng". Hướng đang cân nhắc: *tỉ lệ học viên bổ sung được dẫn chứng còn thiếu ngay trong phiên* · *tỉ lệ học viên nêu được một ví dụ đúng sau khi bị hỏi ngược*.

- Golden set ≥20 case (≥2 case/lớp chỗ khó + 8–10 case thường + 2–4 case hiếm; ≥10 case lấy từ chatlog thật) → `eval/`
- Quality bar: *"Đạt khi ≥ ___% qua bộ, và ___"* — **chưa chốt**

---

## §8. Phân công & kế hoạch

| Họ và tên | Mã học viên | Vai trò chính | Phần việc |
|---|---|---|---|
| Bùi Đức Vinh | 2A202602801 | **Đội trưởng** · Spec & điều phối | Chủ trì `spec.md`; nộp toàn bộ 5 form checkpoint CP1–CP5; chốt lát cắt, non-goals và mức automation; điều phối tiến độ giữa 4 luồng |
| Đinh Công Tú | 2A202602479 | Evidence & mining dữ liệu | Khai thác `tutor_turns.csv` (phương pháp đếm, số liệu ALL vs K4, trích dẫn `turn_id`); viết `evidence/mining-log.md`; chạy khảo sát chuẩn A ≥20 người và giữ log nguyên văn |
| Đỗ Phúc Hưng | 2A202602762 | Prompt & kiểm thử | Thiết kế prompt cho agent học trò; xây golden set ≥20 case trong `eval/`; định nghĩa các chiều chất lượng kiểm chứng được và chạy đo từng lượt |
| Bùi Đức Thông | 2A202602931 | Build & demo | Dựng luồng phiên dạy end-to-end; tích hợp lời gọi AI thật ở quyết định trung tâm; truy xuất đoạn `[T06-xxx]`; quay video CP3 + video dự phòng CP5 |

### Willing users *(≥2 tên, khai từ CP1 — điều kiện tiên quyết của khối R6 ở CP5)*

| Tên | Vai / lớp | Đã đồng ý thử |
|---|---|---|
|  |  |  |
|  |  |  |

> **Track D cần ≥5 người thực sự học một đoạn bằng prototype** ở vòng validation, không chỉ "dùng thử giao diện" — nên khai 6–7 tên ở CP1 để CP5 không thiếu người.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 · CP1 | Chốt Canvas 4 ô, chọn đề D3, loại D1 và D2 | Bảng impact §2 — D3 là ứng viên duy nhất đạt mức Working trong 47,5h và có nguồn đối chiếu sẵn |
| 16/9 · CP1 | Sửa con số "0 lượt chủ động kiểm tra hiểu" thành **1 lượt (0,03%)** | Đọc nguyên văn cả 6 lượt `ask_probing_question` của K4: 2 lượt do học viên tự xin, 3 lượt là gỡ lỗi kỹ thuật. Con số ban đầu không đúng với dữ liệu |
