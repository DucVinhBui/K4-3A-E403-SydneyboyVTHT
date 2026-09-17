# Bằng chứng kiểm thử CP3

## Các file

- `cases.json`: golden set cố định gồm 20 ca. Hai ca sao chép nguồn dùng `mode: "paste"` để lấy nội dung trực tiếp từ `sources.local.json`, tránh commit transcript nội bộ.
- `run-eval.mjs`: chạy golden set và phân loại từng ca thành `ĐẠT`, `CHƯA_ĐẠT`, `LỖI_KỸ_THUẬT` hoặc `CHƯA_CHẠY`.
- `runs/<run-id>.json`: bản ghi bất biến của từng lượt chạy; lượt mới không ghi đè lượt cũ.
- `results.json`: bản sao của lượt chạy gần nhất để giao diện và người chấm tìm nhanh.
- `cp3-measurement.md`: số đo ngắn, có thể dùng làm bằng chứng nộp CP3 khi trường “Đủ điều kiện” là **Có**.

## Chạy

```bash
npm start
npm run eval
```

Muốn kiểm tra cơ chế ghi log mà không gọi API hoặc gửi transcript:

```bash
npm run eval:dry
```

Một lượt chỉ đủ điều kiện nộp khi chạy đủ 20 ca, không có lỗi kỹ thuật và backend báo `sourceMock: false`. Ca trả về sai trạng thái hoặc sai cấu trúc vẫn được tính là đã chạy nhưng `CHƯA_ĐẠT`; không chạy lại riêng ca sai để thay kết quả.
