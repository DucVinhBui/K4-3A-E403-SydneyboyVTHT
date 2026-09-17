# Kịch bản video CP3 — 30 giây

## Thông điệp

> Giải thích lại → bị hỏi ngược đúng chỗ hổng → tự kiểm bằng nguồn.

## Trước khi quay

- Chạy `npm start` và mở `http://127.0.0.1:4173`.
- Kiểm tra đầu trang hiện **AI THẬT** và nguồn không còn nhãn fixture.
- Chạy `npm run eval`; thay `X/20` trong khung hình cuối bằng kết quả thật.
- Chuẩn bị sẵn câu trả lời: “LLM bịa vì nó dự đoán token tiếp theo chứ không tra cứu sự thật.”

## Timeline

- **0–3 giây:** Hiện tên sản phẩm và trạng thái **AI THẬT**. Caption: “Học xong chưa có nghĩa là đã hiểu.”
- **3–7 giây:** Lướt ba tiêu chí và panel nguồn. Caption: “Tiêu chí và nguồn được công bố trước.”
- **7–12 giây:** Dán câu trả lời đã chuẩn bị và bấm **Gửi cho agent học trò**.
- **12–20 giây:** AI trả `THIẾU_CĂN_CỨ` và đúng hai câu hỏi có mã nguồn.
- **20–24 giây:** Bấm mã nguồn để làm sáng đoạn đối chiếu. Caption: “Không đưa đáp án — chỉ hỏi đúng chỗ hổng.”
- **24–27 giây:** Bấm **Bổ sung — giữ nguyên bài mình đã viết**; cho thấy câu cũ vẫn còn.
- **27–30 giây:** Hiện kết quả thật: “20 trường hợp · X trường hợp đạt · Y%”.

Không quay cả bốn nhánh. CP2 đã chứng minh luồng; CP3 cần chứng minh lời gọi AI thật và số đo thật.

