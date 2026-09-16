# Thành viên nhóm — SydneyboyVTHT

**Lớp:** 3A · **Phòng:** E403 · **Cụm:** ____ · **Track:** D — Học tập thích ứng & tương tác trên VLearn · **Đề:** D3 — Học bằng cách dạy

## Bảng phân công

| Họ và tên | Mã học viên | Vai trò chính | Phần việc đảm nhiệm |
|---|---|---|---|
| **Bùi Đức Vinh** | 2A202602801 | **Đội trưởng** · Spec & điều phối | Chủ trì `spec.md`; **nộp toàn bộ 5 form checkpoint CP1–CP5**; chốt lát cắt, non-goals, mức automation; điều phối tiến độ 4 luồng |
| Đinh Công Tú | 2A202602479 | Evidence & mining dữ liệu | Khai thác `tutor_turns.csv` (phương pháp đếm, số liệu ALL vs K4, trích dẫn `turn_id`); viết `evidence/mining-log.md`; chạy khảo sát chuẩn A ≥20 người, giữ log nguyên văn |
| Đỗ Phúc Hưng | 2A202602762 | Prompt & kiểm thử | Thiết kế prompt cho agent học trò; xây golden set ≥20 case trong `eval/`; định nghĩa các chiều chất lượng kiểm chứng được; chạy đo từng lượt và ghi bảng % |
| Bùi Đức Thông | 2A202602931 | Build & demo | Dựng luồng phiên dạy end-to-end; tích hợp lời gọi AI thật ở quyết định trung tâm; truy xuất đoạn `[T06-xxx]`; quay video CP3 và video demo dự phòng CP5 |

## Đội trưởng

**Bùi Đức Vinh — 2A202602801**

Cả 5 mốc CP1–CP5 phải nộp bằng **cùng một mã học viên này**. BTC ghép 5 phiếu của nhóm dựa trên mã học viên người nộp; mốc nào người khác nộp thì hệ thống hiểu là hai nhóm khác nhau và nhóm mất điểm mốc đó. Nếu bất khả kháng phải đổi người nộp, báo coach ngay trong buổi.

## Willing users *(≥2 người ngoài nhóm — khai từ CP1)*

| # | Họ tên | Lớp / vai | Liên hệ | Đã đồng ý thử |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |

> **Track D cần ≥5 người thực sự học một đoạn bằng prototype** ở vòng validation (CP5), không chỉ "dùng thử giao diện" — nên khai 6–7 tên để phòng người bận. Khối R6 (8 điểm) chỉ tính người đã khai từ CP1.

## Ai sở hữu thư mục nào — luật chống conflict

**Một người một thư mục. Không ai sửa file của người khác.** Cần đổi gì trong phần người khác thì nhắn cho họ, đừng tự sửa.

| Người | Sở hữu | Khối điểm nằm ở đây |
|---|---|---|
| **Vinh** | `spec.md` · `README.md` · `teammates.md` · slide CP5 | R2 lát cắt 15 · R3 chỗ khó 11 |
| **Tú** | `evidence/` · `validation/` | R1 bằng chứng 15 · **R6 người thử 8** |
| **Hưng** | `eval/` | **R4 kiểm thử 15** |
| **Thông** | `codebase/` · `.gitignore` | R5 prototype 8 |
| *(mỗi người)* | `reflection/<tên>.md` của riêng mình | điều kiện nộp bài |

### Ba lệnh, lần nào cũng đúng thứ tự này

```bash
git pull --rebase origin main      # 1. lấy việc người khác về TRƯỚC
git add evidence/                  # 2. CHỈ thư mục của mình
git commit -m "viết gì làm nấy"
git push origin main               # 3. đẩy lên
```

> ❌ **Không bao giờ gõ `git add .` hoặc `git add -A`.** Repo này public. Một lần `git add .` khi máy đang có data pack là cả khoá lộ lên mạng. Luôn gõ rõ tên thư mục của mình.

> Nếu `push` bị từ chối (*non-fast-forward*): chạy lại `git pull --rebase origin main` rồi push. Không dùng `--force`.

---

## Việc từng người — mỗi gạch đầu dòng là một commit

Xếp theo hạn. Làm xong gạch nào, commit gạch đó luôn, đừng gom.

### Đinh Công Tú — `evidence/` + `validation/` *(23 điểm, nặng nhất nhóm)*

| # | File cần tạo | Nội dung | Hạn |
|---|---|---|---|
| 1 | `validation/willing-users.md` | 6–7 người ngoài nhóm: tên · lớp · liên hệ · đã đồng ý chưa. **Làm trước tiên** — R6 chỉ tính người khai sớm | tối nay |
| 2 | `evidence/survey-log.md` | Log nguyên văn khảo sát: từng người trả lời gì ở C1–C4, chép nguyên văn C5/C6. Cuối file chốt bảng `n · số xác nhận · tỉ lệ %` theo đúng định nghĩa đã khoá ở `survey-questions.md` | trước **21:00 17/9** |
| 3 | `validation/plan.md` | Kịch bản buổi thử: mời ai, ngồi bao lâu, hỏi gì **trước** khi dùng, đo gì **sau** khi dùng | 17/9 |
| 4–8 | `validation/session-01.md` … `session-05.md` | Mỗi buổi thử **một file = một commit**. Ghi: người đó học đoạn nào, làm được gì, kẹt ở đâu, nói câu gì | trước **13:00 18/9** |

> Track D bắt buộc **≥5 người thật sự học một đoạn** bằng prototype, không phải bấm thử giao diện. Đây là chỗ dễ mất trắng 8 điểm nhất nếu để sát giờ.

### Đỗ Phúc Hưng — `eval/` *(15 điểm — khối đang trống hoàn toàn)*

| # | File cần tạo | Nội dung | Hạn |
|---|---|---|---|
| 1 | `eval/golden-set.md` | **≥20 case**: ≥2 case cho mỗi lớp trong 4 lớp chỗ khó (§5 của spec) + 8–10 case thường + 2–4 case hiếm. Mỗi case: input học viên gõ → trạng thái mong đợi → vì sao | tối nay / sáng 17/9 |
| 2 | `eval/quality-bar.md` | Chốt *"đạt là gì"*. **Bắt buộc có ≥1 chỉ số về việc HỌC**, không chỉ "AI trả lời đúng" — ví dụ *tỉ lệ học viên bổ sung được dẫn chứng còn thiếu ngay trong phiên* | trước **21:00 17/9** |
| 3 | `eval/prompt-v1.md` | Prompt cho agent học trò: persona, cấm đưa đáp án, bắt buộc gắn mã `[T06-xxx]`, cách trả về 1 trong 3 trạng thái | 17/9 |
| 4 | `eval/run-01.md` | Chạy hết 20 case, ghi **từng case** đúng/sai → ra con số *"thử N, đúng M"* mà **CP3 bắt nộp** | trước **16:00 17/9** |
| 5 | `eval/run-02.md` | Sửa prompt rồi chạy lại, so với run-01 | 17/9 |

### Bùi Đức Thông — `codebase/` *(8 điểm + video CP3)*

| # | Việc | Hạn |
|---|---|---|
| 1 | Thay hàm `decide()` trong `prototype/index.html` bằng **lời gọi AI thật**. Ô nhập API key đặt ở màn M1, **key không được commit** | trước **16:00 17/9** |
| 2 | Đọc đoạn nguồn thật từ `sources.local.json` *(đã chặn trong `.gitignore`)*, giữ fixture `MOCK` làm bản dự phòng khi không có file đó — **không commit nội dung transcript thật** | 17/9 |
| 3 | Quay **video thao tác 30 giây**, để link vào `codebase/demo-cp3.md` | trước **16:00 17/9** |
| 4 | Cập nhật bảng mock/thật trong `codebase/README.md` sau khi cắm AI xong | 17/9 |
| 5 | Quay **video demo dự phòng** cho buổi pitch | trước **13:00 18/9** |

### Bùi Đức Vinh — `spec.md` + điều phối

| # | Việc | Hạn |
|---|---|---|
| 1 | §5 nâng từ 4 lên **≥8 kịch bản** — R3 là 11 điểm, hiện mới có một nửa | trước **21:00 17/9** |
| 2 | §7 chép quality bar từ `eval/quality-bar.md` của Hưng vào và **khoá lại** | trước **21:00 17/9** |
| 3 | §1 điền kết quả khảo sát từ `evidence/survey-log.md` của Tú | 17/9 |
| 4 | §9 Changelog — ghi **≥1 thay đổi** kèm lý do | liên tục |
| 5 | Slide PDF | trước **13:00 18/9** |
| 6 | **Nộp cả 5 form CP1–CP5** bằng mã `2A202602801` | từng mốc |

### Cả bốn người — `reflection/<tên>.md`

Một file cho mỗi người, tự viết, tự commit: vai trò · phần mình làm · AI hỗ trợ thế nào · **một bài học rút từ case fail của chính nhóm**. Hạn trước **13:00 18/9**.

---

## Luật áp cho mọi thành viên

**Vibe-coding rule.** Dùng AI để build thoải mái, nhưng giám khảo có thể hỏi **bất kỳ ai** về phần có tên người đó trong bảng trên. Không giải thích được thì phần đó **0 điểm**.

**Reflection cá nhân.** Mỗi người một file trong `reflection/`: vai trò · phần mình làm · AI hỗ trợ thế nào · một bài học từ case fail của chính nhóm.

---

*Bảng này còn xuất hiện ở `README.md` (đầu file) và `spec.md` §8 — sửa tên hoặc phần việc thì sửa cả ba chỗ.*
