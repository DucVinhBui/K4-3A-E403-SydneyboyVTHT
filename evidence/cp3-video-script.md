# Kịch bản video CP3 — 30 giây

## Thông điệp

> Giải thích lại → bị hỏi ngược đúng chỗ hổng → tự kiểm bằng nguồn.

---

## ⚠️ Lệnh chạy — ĐỌC KỸ, đã đổi ngày 17/9

Bản mẫu hiện gọi 5 endpoint (`/api/config`, `/api/decide`, `/api/eval/cases`, `/api/eval/run`, `/api/flow`).
**Chỉ server Python phục vụ đủ cả 5.** `npm start` / cổng `4173` là stack cũ của CP2 — chạy sẽ 404 giữa lúc quay.

### 1. Đặt khoá — bắt buộc, nếu không thanh trạng thái hiện `MOCK`

Tạo file `codebase/.env` (đã bị `.gitignore` chặn, không bao giờ commit):

```
MINILAB_PROVIDER=openrouter
MINILAB_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=<khoá thật>
```

### 2. Chạy server

```bash
cd codebase && python3 -m api.server --port 8765
```

### 3. Mở `http://127.0.0.1:8765`

### 4. Kiểm 3 thứ TRƯỚC khi bấm quay

- [ ] Thanh trạng thái góc phải hiện **`OPENROUTER · OPENAI/GPT-4O-MINI`** — **không phải** `BẢN MẪU — MOCK`. Còn chữ MOCK là khoá chưa vào, quay là hỏng.
- [ ] Bấm thử một câu, thấy agent trả về có mã `[T06-xxx]` thật.
- [ ] Khung hình cuối điền đúng **25 case · 21 đạt · 84%** (số chính thức, xem `codebase/eval/run_results.md`).

---

## Timeline 30 giây

| Giây | Việc | Caption |
|---|---|---|
| 0–3 | Hiện tên sản phẩm + thanh trạng thái **OPENROUTER · GPT-4O-MINI** | "Học xong chưa có nghĩa là đã hiểu." |
| 3–7 | Lướt ba tiêu chí ở M1 và panel nguồn bên phải | "Tiêu chí và nguồn được công bố trước." |
| 7–12 | Dán câu đã chuẩn bị, bấm **Gửi cho agent học trò** | |
| 12–20 | AI trả `THIẾU_CĂN_CỨ` + đúng hai câu hỏi ngược có mã nguồn | |
| 20–24 | Bấm mã nguồn → đoạn đối chiếu sáng lên | "Không đưa đáp án — chỉ hỏi đúng chỗ hổng." |
| 24–27 | Bấm **Bổ sung — giữ nguyên bài mình đã viết**, cho thấy câu cũ còn nguyên | |
| 27–30 | Hiện số thật: **"25 trường hợp · 21 đạt · 84%"** | |

**Câu chuẩn bị sẵn để dán** (cố tình thiếu ý c2 và c3 để agent hỏi ngược):

> LLM bịa vì nó dự đoán token tiếp theo chứ không tra cứu sự thật.

Không quay cả bốn nhánh. CP2 đã chứng minh luồng; CP3 cần chứng minh **lời gọi AI thật** và **số đo thật**.

---

## Số nộp kèm form CP3

> Chạy **25** trường hợp qua `gpt-4o-mini` (OpenRouter), **21** đạt — **84,0%**.
> Đã chạy 2 lượt: run-01 56% → sửa system prompt → run-02 84%. Giữ nguyên cả 4 case fail, không chọn lượt đẹp hơn.
> Chi tiết từng case: `codebase/eval/run_results.md`.
