# Nhật ký cho người ngoài dùng thử — khối R6

**Trạng thái:** ⛔ **chưa chạy** — 0 người, 0 phiên, 0 quote. Khung này dựng sẵn để điền tại chỗ.

Khai đầy đủ ở [`spec.md` §10](../spec.md) mục 1. Không có thư mục này thì trần điểm của nhóm là **92**.

---

## Luật thu dữ liệu — đọc trước khi mời người thử

**Giao task rồi ngồi im xem họ làm. Đừng hỏi “sản phẩm này hay không”.**
Quote ăn điểm là lời người ta buột ra **lúc đang cố làm việc**, không phải lời nhận xét lúc đã làm xong.

| Quote chưa đạt | Quote đạt |
|---|---|
| *“Demo này ok rồi đấy”* | *“Mình muốn tìm thông tin về code cho ReAct”* |

**Chép đúng nguyên văn, kể cả sai chính tả, kể cả câu chê.**
Người dùng chê vẫn **đủ điểm** — mục đích là xem giải pháp có ăn thua không, ra kết quả nào cũng ghi nhận.

**Chỉ lưu tên người đã đồng ý cho thử và quote nguyên văn. Không lưu gì thêm** — không email, không số điện thoại, không ảnh chụp màn hình có thông tin cá nhân.

---

## Task giao cho người thử

Đây là track D, nên phải là **học thật một đoạn**, không phải bấm thử giao diện.

1. Đưa họ đọc đoạn nguồn về **“vì sao LLM bịa”** trong bản mẫu (panel bên phải, các mã `[T06-xxx]`).
2. Bảo họ: *“Giải thích lại cho mình nghe vì sao LLM bịa, bằng lời của bạn.”* — gõ vào ô nhập, bấm gửi.
3. **Ngồi im.** Agent sẽ hỏi ngược 2 câu. Xem họ có quay lại bổ sung không, hay bỏ cuộc.
4. Ghi lại **đúng một điều**: sau khi bị hỏi ngược, họ có **bổ sung được ít nhất một dẫn chứng còn thiếu** không?

Bước 4 chính là **điều kiện 4 của Quality Bar** (`spec.md` §7) — ngưỡng đã khoá từ CP4:
**≥ 60% người thử bổ sung được ≥ 1 dẫn chứng, n ≥ 5.** Không sửa ngưỡng sau khi thấy số.

Chạy bản mẫu:

```bash
cd codebase && ../.venv/bin/python -m api.server --port 8765
```

Kiểm badge trên thanh tiêu đề đã chuyển **xanh có chấm tròn** rồi mới cho người ta thử — badge đỏ `BẢN MẪU — MOCK` nghĩa là đang chạy heuristic cũ, không phải AI thật.

---

## Bảng nhật ký

Cần **5 người ngoài nhóm**, trong đó **2 người đã khai từ CP1** (`teammates.md` → Willing users).

| # | Ai thử | Đã khai CP1? | Task được giao | Kẹt ở đâu | Quote nguyên văn | Sau khi bị hỏi ngược có bổ sung được dẫn chứng? | Quyết định của nhóm |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |

**Cột “có bổ sung được dẫn chứng?”** chỉ điền `có` / `không`. Đếm xong ghi kết quả xuống đây:

> **Điều kiện 4 — chỉ số HỌC:** ___ / 5 người = ___%  · ngưỡng ≥ 60%, n ≥ 5 → **đạt / không đạt**

---

## Bốn dòng tổng kết — bắt buộc

1. **Chủ đề lặp nhiều nhất:**
2. **Sẽ sửa gì trước demo:**
3. **Giữ nguyên gì và vì sao:**
4. **Gì để dành sau:**

---

## Ít nhất một thay đổi

Rubric đòi **tối thiểu 1 thay đổi** rút ra từ vòng này, ghi vào **§9 Changelog** của `spec.md`.
Nếu quyết định **giữ nguyên** thì vẫn phải ghi, kèm lý do — im lặng mới bị trừ.

| Thay đổi | Rút ra từ quote nào | Đã ghi vào §9 chưa |
|---|---|---|
|  |  |  |
