# Kịch bản video CP3 — 30 giây

## Thông điệp

> Giải thích lại → bị hỏi ngược đúng chỗ hổng → tự kiểm bằng nguồn.

Không quay cả bốn nhánh. CP2 đã chứng minh luồng; CP3 chỉ cần chứng minh
**lời gọi AI thật** và **số đo thật**.

---

## A · Dựng sân — làm trước, chưa quay

### 1. Khoá API

File `codebase/.env` (đã bị `.gitignore` chặn, không bao giờ commit):

```
MINILAB_PROVIDER=openai
MINILAB_MODEL=gpt-4o-mini
OPENAI_API_KEY=<khoá thật>
MINILAB_MAX_TOOL_HOPS=6
```

### 2. Chạy server

```bash
cd /Users/ducvinhbui/Desktop/Vin_AI/K4-3A-E403-SydneyboyVTHT/codebase && ../.venv/bin/python -m api.server --port 8765
```

Bắt buộc `../.venv/bin/python`. Dùng `python3` của anaconda sẽ lỗi
`APIConnectionError` vì xung đột httpx. Cổng `4173` / `npm start` là stack Node
cũ của CP2, thiếu 3 trong 5 endpoint — chạy sẽ 404 giữa lúc quay.

### 3. Tự kiểm bằng máy, đừng kiểm bằng mắt

```bash
cd /Users/ducvinhbui/Desktop/Vin_AI/K4-3A-E403-SydneyboyVTHT/codebase && ../.venv/bin/python -m eval.run_demo_check
```

Lệnh này bắn đúng bốn câu nằm sau bốn nút demo vào server đang chạy, cộng một
câu lạc đề gõ tay. Phải thấy:

```
✅ Provider: openai / gpt-4o-mini
✅ ① Trả lời đủ ý             → ĐỦ_CĂN_CỨ
✅ ② Trả lời thiếu ý          → THIẾU_CĂN_CỨ  ['T06-141', 'T06-145']
✅ ③ Nói sang chuyện khác     → NGOÀI_PHẠM_VI
✅ ④ Dán nguyên văn           → THIẾU_CĂN_CỨ
✅ (gõ tay) mỳ cay            → NGOÀI_PHẠM_VI
✅ Bốn nhánh chạy đúng. Quay được.
```

Còn một dấu ❌ thì **đừng bấm quay**. Nó cũng in thời gian mỗi lượt gọi —
đo ngày 17/9 là **1,4–4,8 giây**, trung bình 2,6s.

### 4. Ba thứ nhìn bằng mắt trước khi bấm quay

- [ ] Badge góc phải hiện **`OPENAI · gpt-4o-mini`** — không phải `BẢN MẪU — MOCK`
- [ ] Cột phải hiện đủ 4 đoạn `[T06-138]` … `[T06-149]`
- [ ] Đóng hết tab khác, ẩn thanh bookmark, phóng trình duyệt 110–125%

---

## B · Timeline 30 giây

Chỉ có **một** lượt chờ AI trong cả video. Đó là lý do bố cục dưới đây bám
vào một lần bấm Gửi duy nhất.

| Giây | Bấm gì | Màn hình có gì | Caption |
|---|---|---|---|
| 0–4 | Đứng yên ở M1 | Tên sản phẩm + badge `OPENAI · gpt-4o-mini` | "Học xong chưa có nghĩa là đã hiểu." |
| 4–7 | Lướt xuống ba tiêu chí, hất mắt sang cột nguồn bên phải | 3 tiêu chí + 4 đoạn `[T06-xxx]` | "Tiêu chí và nguồn công bố trước, không đổi giữa phiên." |
| 7–9 | Bấm **Bắt đầu dạy lại** → bấm nút **② Trả lời thiếu ý** | Câu mẫu tự điền vào ô | |
| 9–11 | Bấm **Gửi cho agent học trò** | Nút đổi thành *Đang gọi agent…* | |
| 11–15 | *(chờ AI — đo được 3,8s)* | | "Quyết định do AI thật đưa ra, không phải if-else." |
| 15–22 | Không bấm gì, để người xem đọc | Chip **`THIẾU_CĂN_CỨ`** + đúng **2 câu hỏi ngược**, mỗi câu gắn `[T06-141]` / `[T06-145]` | "Không đưa đáp án — chỉ hỏi đúng chỗ hổng." |
| 22–25 | Bấm chữ `[T06-141]` dưới câu hỏi 1 | Đoạn nguồn tương ứng sáng lên ở cột phải | "Mỗi câu hỏi truy được về nguồn." |
| 25–27 | Bấm **Bổ sung — giữ nguyên bài mình đã viết** | Quay lại M2, **bài cũ còn nguyên chữ** | "Sửa không phải gõ lại từ đầu." |
| 27–30 | Cắt sang khung số | **25 ca · 24 đạt · 96%** | |

### Câu dùng để quay

Bấm nút **② Trả lời thiếu ý**, đừng gõ tay — gõ tay tốn 6–8 giây trong khi cả
video chỉ có 30.

> LLM sinh câu bằng cách dự đoán token tiếp theo theo xác suất.

Câu này cố tình chỉ chạm tiêu chí c1. Đã chạy 3 lượt liên tiếp, lượt nào cũng
ra `THIẾU_CĂN_CỨ` + đúng 2 câu hỏi ngược gắn `[T06-141]` và `[T06-145]`.

### Nếu lỡ tay

- Bấm nhầm **① Trả lời đủ ý** → ra `ĐỦ_CĂN_CỨ`, không có câu hỏi ngược. Quay lại.
- Trang đứng im khi bấm Gửi → mở Console, xem có `ReferenceError` không, rồi
  chạy lại `run_demo_check`.
- Badge hiện `BẢN MẪU — MOCK` → server chưa đọc được `.env`. Tắt server, kiểm
  `codebase/.env`, chạy lại.

---

## C · Số nộp kèm form CP3

> Chạy **25** trường hợp qua `gpt-4o-mini` (OpenAI trực tiếp), **24** đạt — **96,0%**.
> Bộ đo thứ hai trên knowledge base: **45 ca · 45 đạt · 100%**, trong đó 0/45 ca
> agent trích ra mã đoạn không có thật.
> Đã chạy 4 lượt: 56% → 84% → 64% → 96%. Lượt 64% là một lần sửa đi sai, bộ đo
> khoá trước bắt được; giữ nguyên trong báo cáo. Không chọn lượt chạy đẹp hơn.
> Chi tiết từng ca: `codebase/eval/run_results.md`.
