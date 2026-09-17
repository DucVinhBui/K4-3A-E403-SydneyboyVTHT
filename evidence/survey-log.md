# Nhật ký khảo sát chuẩn A

**Khảo sát:** Cách mọi người học trong khoá AI20k<br>
**Nguồn:** [Google Form](https://docs.google.com/forms/d/14juAFGo64X_ekgWMhwQxPh24NBebLL7rNsDRf7BD9fw/edit?no_redirect=true#responses) · bộ câu hỏi tại [survey-questions.md](survey-questions.md)<br>
**Ngày trích dữ liệu:** 16/09/2026<br>
**Người phụ trách:** Đinh Công Tú — `2A202602479`<br>
**Mục tiêu chuẩn A:** ít nhất 20 người ngoài nhóm và hơn 50% số người thỏa định nghĩa xác nhận đã khóa trước khi phát form.<br>
**Số lượt gửi trên Form:** 24<br>
**Số người duy nhất sau lọc trùng:** 23<br>
**Số người ngoài nhóm có thể xác minh:** 20

> Log này không lưu thời gian gửi của từng câu trả lời. Các câu C5 và C6 được giữ nguyên văn, kể cả lỗi chính tả; câu không có nội dung được ghi là `*(bỏ trống)*`.

## 1. Quy tắc tính chuẩn A

Theo định nghĩa đã khóa trong `spec.md`, một người chỉ được tính là **xác nhận** khi đồng thời thỏa:

1. C2 là **“Thấy quen, đọc trôi được”** hoặc **“Đọc lại thấy ổn”** — điều kiện `(a)`.
2. C3 là **“Có — tôi kể lại được lần đó”** — điều kiện `(b)`.

Kết quả của từng người là `a ∧ b`. Ngưỡng đạt là `n ≥ 20` người ngoài nhóm và tỉ lệ xác nhận `> 50%`.

Quy tắc lọc:

- Loại một lượt gửi trùng hoàn toàn của Lê Phan Việt Cường.
- Loại Đỗ Phúc Hưng và Đinh Công Tú vì là thành viên nhóm theo `README.md`.
- Loại Nguyễn Trọng Phúc khỏi mẫu tính chuẩn A vì không có mã học viên, nên không thể xác minh là người ngoài nhóm.
- Không đặt thêm điều kiện loại dựa trên nội dung sau khi đã xem dữ liệu.

## 2. Log từng phiếu sau lọc trùng

| # Form | Họ tên + mã học viên | Tư cách khi tính chuẩn A | C1 | C2 | C3 | C4 | `a∧b` | C5 — nguyên văn | C6 — nguyên văn |
|---:|---|---|---|---|---|---|:---:|---|---|
| 1 | Lê Phan Việt Cường — `2A202602641` | Ngoài nhóm, hợp lệ | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — nhưng không nhớ rõ lần nào | Ngại hỏi / mất tự tin | Không | Học lec1 | *(bỏ trống)* |
| 2 | Đỗ Phúc Hưng — *(không cung cấp mã)* | Thành viên nhóm — loại | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — nhưng không nhớ rõ lần nào | Mất thời gian làm lại; Ngại hỏi / mất tự tin | Không | tôi học Transformet, hiểu khá sau | không |
| 3 | Đinh Công Tú — `2A202602479` | Thành viên nhóm — loại | Hỏi AI tutor trên VLearn | Đọc lại thấy ổn | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz; Mất thời gian làm lại | Không | Khái niệm chung chung, đọc lại không hiểu sâu | Có cần người huongws dẫn, kiểm tra lại |
| 4 | Bùi Gia Chính — `2A202602693` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz | Không | Khi học về các nội dung buổi 1, 2, tôi trả lời sai khái niệm ở quiz ôn tập | *(bỏ trống)* |
| 5 | Nguyễn Ngọc Thái An — `2A202602462` | Ngoài nhóm, hợp lệ | Đọc lại slide một lượt nữa | Đọc lại thấy ổn | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz | Không | Phát hiện nhớ nhầm về attention trong transformer<br>Phát hiện ra lúc search lại trên mạng | *(bỏ trống)* |
| 7 | Trần Thị Thu Trang — `2A202602581` | Ngoài nhóm, hợp lệ | Đọc lại slide một lượt nữa | Đọc lại thấy ổn | Có — tôi kể lại được lần đó | Mất thời gian làm lại; Hiểu sai kéo sang các bài sau | **Có** | Tôi học attention và nghĩ mỗi token chỉ chú ý một token khác. Đến lúc làm quiz tôi mới phát hiện cách hiểu đó sai. | Có, khi tôi tự làm đúng nhiều bài tập liên tiếp về tokenization. |
| 8 | Lê Văn Sang — `2A202602391` | Ngoài nhóm, hợp lệ | Hỏi AI tutor trên VLearn | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Ngại hỏi / mất tự tin | Không | Tôi học transformer nhưng đọc xong vẫn nhầm vai trò encoder và decoder. Sau đó xem lại ví dụ tôi mới nhận ra. | Không, tôi thường cần một người hỏi lại để biết mình hiểu tới đâu. |
| 9 | Nguyễn Trọng Phúc — *(không cung cấp mã)* | Không xác minh được — loại | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — tôi kể lại được lần đó | Mất thời gian làm lại; Hiểu sai kéo sang các bài sau | Không | Học attention hiểu sai cơ chế attention phát hiện khi tự review | Không |
| 10 | Phạm Văn Hoàng Anh Tú — `2A202602507` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Hiểu sai kéo sang các bài sau | Không | Học toán, sai về công thức tính hàm, lúc làm bài tập | Ko đủ, cần bạn bè kiểm tra check chéo lại |
| 11 | Kiêu Đình Đoàn — `2A202602936` | Ngoài nhóm, hợp lệ | Tự làm bài tập/quiz về nó | Có người kiểm tra lại và xác nhận | Có — tôi kể lại được lần đó | Ngại hỏi / mất tự tin; Không mất gì đáng kể | Không | Tôi nghĩ RAG là kiểu model tự học thêm kiến thức mới | Đủ, cần tự luyện tập cá nhâ, kiểm tra lại đáp án sau khi làm |
| 12 | Đoàn Quang Thắng — `2A202602395` | Ngoài nhóm, hợp lệ | Giải thích lại cho bạn khác | Giải thích lại được cho người khác | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz | Không | không nhớ | chịu |
| 13 | Trân Thê Anh — `2A202602516` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Hiểu sai kéo sang các bài sau | Không | Không nhớ rõ | Có. Nếu tôi giải thích lại được cho người khác, người ta hỏi lại vài câu mà tôi vẫn trả lời được thì tôi thấy khá đủ. |
| 14 | Nguyễn Khánh Duy — `2A202602403` | Ngoài nhóm, hợp lệ | Hỏi AI tutor trên VLearn | Tự làm được bài tập về nó | Có — nhưng không nhớ rõ lần nào | Mất thời gian làm lại; Hiểu sai kéo sang các bài sau; Ngại hỏi / mất tự tin | Không | ko nhớ | xem ytb để cải thiện hiểu biết, không muốn hỏi người khác |
| 15 | Nguyễn Phương Nam — `2A202602869` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Chưa bao giờ | Không mất gì đáng kể; Chưa từng xảy ra | Không | Không có | Cách học hiện tại tôi thấy đủ, k cần cải thiện thêm |
| 16 | Lê Hoàng Thiên Phú — `2A202602908` | Ngoài nhóm, hợp lệ | Tự làm bài tập/quiz về nó | Tự làm được bài tập về nó | Có — tôi kể lại được lần đó | Mất điểm bài tập/quiz; Mất thời gian làm lại | Không | Học về RAG, tôi chỉ hiểu bề mặt của chúng, các giai đoạn cần có khi triển khai RAG, nhưng cốt lõi về thuật toán, model tôi chưa đào sâu, khiến việc làm dự án bị sơ sài | Cần cải thiện thêm, tự học thêm |
| 17 | Nguyễn Văn Tài — `2A202603004` | Ngoài nhóm, hợp lệ | Đọc lại slide một lượt nữa | Thấy quen, đọc trôi được | Có — tôi kể lại được lần đó | Mất điểm bài tập/quiz; Mất thời gian làm lại | **Có** | system prompt với user prompt ngang quyền nhau. Đến lúc cố tình viết 2 prompt mâu thuẫn rồi test mới thấy system được ưu tiên hơn. | có, khi test thử được nhiều case khác nhau mà kết quả vẫn đúng như mình dự đoán |
| 18 | Lương Quang Huy — `2A202602698` | Ngoài nhóm, hợp lệ | Hỏi AI tutor trên VLearn | Có người kiểm tra lại và xác nhận | Có — tôi kể lại được lần đó | Không mất gì đáng kể | Không | hiểu sai một đoạn ở transformer nhưng không nhớ chính xác, lúc làm bài hoặc được giải thích lại thì mới biết | Không, tôi hay cần người khác hỏi ngược lại |
| 19 | Lê Văn Tài — `2A202602464` | Ngoài nhóm, hợp lệ | ngồi chơi :))) | I am the best | Chưa bao giờ | Chưa từng xảy ra | Không | Mình quá đẳng cấp, ko hiểu sai chỗ nào | Bài quá dễ |
| 20 | Phan Trọng Hoàn — `2A202602954` | Ngoài nhóm, hợp lệ | Đọc lại slide một lượt nữa | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Hiểu sai kéo sang các bài sau; Ngại hỏi / mất tự tin | Không | tôi từng nói với bạn là agent chỉ là chatbot có prompt tốt hơn, bạn hỏi thế tool call với vòng lặp action nằm ở đâu và tôi ko trả lời đc | Có, nhất là khi người nghe hỏi thêm mà t vẫn giải thích được bằng ví dụ khác |
| 21 | Nguyễn Huy HÙng — `2A202602990` | Ngoài nhóm, hợp lệ | Giải thích lại cho bạn khác | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz; Mất thời gian làm lại; Hiểu sai kéo sang các bài sau | Không | không nhớ rõ, trả lời câu hỏi của thầy nhưng sai | đủ rồi |
| 22 | Nguyễn Mạnh Hải — `2A202602988` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Thấy quen, đọc trôi được | Có — nhưng không nhớ rõ lần nào | Mất điểm bài tập/quiz; Mất thời gian làm lại | Không | học lec2, bị trôi kiến thức do dài, lúc làm quizz sai nhiều | ko đủ, cần học lại nhiều lần bằng cách xem lai bài giảng |
| 23 | Võ Phú Hãn — `2A202602628` | Ngoài nhóm, hợp lệ | Giải thích lại cho bạn khác | Có người kiểm tra lại và xác nhận | Có — nhưng không nhớ rõ lần nào | Không mất gì đáng kể | Không | làm bài tự luyện tập, có thể làm nhiều lần , phát hiện sai do đọc chưa kỹ | cũng đủ, do tôi luyện tập nhiều |
| 24 | Vũ Duy Điệp — `2A202602703` | Ngoài nhóm, hợp lệ | Đi thẳng sang phần tiếp theo | Tự làm được bài tập về nó | Có — tôi kể lại được lần đó | Mất thời gian làm lại | Không | tự luyện tập trên vlearn, làm sai nhiều lần bài chắc nghiệm | khá đủ, do luyện tập làm đc cho đến khi đúng thì thôi |

Phiếu số 6 là lượt gửi thứ hai của **Lê Phan Việt Cường — `2A202602641`**, trùng hoàn toàn C1–C6 với phiếu số 1 nên không lặp lại trong bảng.

## 3. Kết quả theo ngưỡng đã khóa

- Lượt gửi thô: **24**.
- Phiếu trùng bị loại: **1**.
- Người duy nhất sau lọc trùng: **23**.
- Thành viên nhóm bị loại: **2**.
- Phiếu không đủ mã để xác minh người ngoài nhóm: **1**.
- Mẫu hợp lệ ngoài nhóm: **20**.
- Thỏa điều kiện `(a)`: **11/20**.
- Thỏa điều kiện `(b)`: **6/20**.
- Thỏa đồng thời `a ∧ b`: **2/20** — Trần Thị Thu Trang và Nguyễn Văn Tài.
- **Tỉ lệ xác nhận: 10%**.
- **Kết luận: không đạt chuẩn A.** Mẫu đã đạt `n ≥ 20`, nhưng 10% không lớn hơn ngưỡng 50% đã khóa trước khi phát Form.

Kết quả này không ủng hộ giả định rằng hơn một nửa người học vừa dựa vào cảm giác đọc trôi/đọc lại thấy ổn, vừa kể lại được một lần họ phát hiện mình đã hiểu sai. Theo `spec.md`, nhóm cần ghi nhận kết quả fail này và xem lại giả định vấn đề hoặc cách đặt tiêu chí; không được đổi định nghĩa xác nhận sau khi đã xem dữ liệu.

## 4. Đối chiếu nhanh với bản tóm tắt của Google Form

Các số đếm trên 24 lượt gửi thô:

- C1: đi thẳng **6**; đọc lại slide **4**; hỏi AI tutor **8**; tự làm bài/quiz **2**; giải thích cho bạn **3**; khác **1**.
- C2: thấy quen/đọc trôi **9**; đọc lại thấy ổn **3**; tự làm được bài **7**; giải thích lại được **1**; có người kiểm tra **3**; khác **1**.
- C3: kể lại được lần hiểu sai **7**; có nhưng không nhớ rõ **15**; chưa bao giờ **2**.
- C4: mất điểm **8**; mất thời gian **10**; hiểu sai kéo sang bài sau **7**; ngại hỏi/mất tự tin **7**; không mất gì đáng kể **4**; chưa từng xảy ra **2**.

Các số này dùng để kiểm tra việc chép dữ liệu, không thay thế phép tính trên mẫu 20 người ngoài nhóm hợp lệ.

## 5. Năm câu C5 nguyên văn từ người ngoài nhóm đã xác minh

> “Tôi học attention và nghĩ mỗi token chỉ chú ý một token khác. Đến lúc làm quiz tôi mới phát hiện cách hiểu đó sai.”  
> — Trần Thị Thu Trang

> “system prompt với user prompt ngang quyền nhau. Đến lúc cố tình viết 2 prompt mâu thuẫn rồi test mới thấy system được ưu tiên hơn.”  
> — Nguyễn Văn Tài

> “tôi từng nói với bạn là agent chỉ là chatbot có prompt tốt hơn, bạn hỏi thế tool call với vòng lặp action nằm ở đâu và tôi ko trả lời đc”  
> — Phan Trọng Hoàn

> “Khi học về các nội dung buổi 1, 2, tôi trả lời sai khái niệm ở quiz ôn tập”  
> — Bùi Gia Chính

> “Phát hiện nhớ nhầm về attention trong transformer  
> Phát hiện ra lúc search lại trên mạng”  
> — Nguyễn Ngọc Thái An
