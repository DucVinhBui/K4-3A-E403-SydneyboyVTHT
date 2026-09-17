# Kết quả chạy Golden Set qua LLM thật — CP3

**Provider:** `openrouter` · **Model:** `openai/gpt-4o-mini` (qua OpenRouter, API tương thích OpenAI)
**Ngày chạy:** 17/9/2026 · **Script:** [`eval/run_golden.py`](run_golden.py) · **Dữ liệu:** [`eval/golden_set.json`](golden_set.json) (25 case)
**Log thô prompt + response:** [`logs/llm_calls.jsonl`](../logs/llm_calls.jsonl) — mỗi lời gọi LLM (kể cả các bước tool-calling) được ghi một dòng JSON, gồm toàn bộ `messages` gửi đi và `raw_response` nhận về từ API.

Nhóm chạy **hai lượt (run-01 → sửa prompt → run-02)** đúng quy trình đã định trong `teammates.md`. Cả hai lượt dùng chung `golden_set.json` và chung provider/model, chỉ khác `agent/prompts.py`.

## 1. Bảng so sánh run-01 vs run-02

| Chỉ số | run-01 (prompt gốc) | run-02 (prompt đã sửa) |
|---|---|---|
| Tổng số case | 25 | 25 |
| Số case ĐẠT | 14 | **21** |
| Số case THẤT BẠI | 11 | **4** |
| **Tỷ lệ đạt** | 56,0% | **84,0%** |

Kết quả raw đầy đủ từng case: [`eval/run_results_raw.json`](run_results_raw.json) (run-01) và [`eval/run_results_raw_v2.json`](run_results_raw_v2.json) (run-02).

Tiêu chí "ĐẠT" một case (theo `golden_set.json._meta.acceptance_criteria`):
1. `decision.state` khớp `expected_state`, **VÀ**
2. nếu `expected_verbatim=true` thì `decision.is_verbatim_paste` cũng phải `true`, **VÀ**
3. mọi `source_id` trong `decision.probes` phải là mã hợp lệ trong `EXCERPTS` (agent không bịa mã đoạn).

## 2. Thay đổi giữa run-01 và run-02

Sau khi đọc log run-01, nhóm phát hiện nguyên nhân gốc: system prompt (`agent/prompts.py`) định nghĩa `NGOÀI_PHẠM_VI` là "không chạm tiêu chí nào **VÀ** nói sang thứ không có trong 4 đoạn" — hai điều kiện phải cùng đúng, nhưng mô hình chỉ kiểm tra điều kiện đầu rồi gán luôn `NGOÀI_PHẠM_VI`, không phân biệt được "học viên không nói gì để chấm" với "học viên nói sang chuyện khác".

Sửa: viết lại rõ ràng hơn trong `SYSTEM_PROMPT`:
- `THIẾU_CĂN_CỨ` bổ sung thêm trường hợp: học viên không đưa lời giải thích nào (xin đáp án, xin giảng lại, xin làm hộ, bối rối) hoặc đang **cố trả lời sai** câu hỏi đang hỏi (kể cả nhân cách hoá mô hình, đổ lỗi hạ tầng/bug) — vẫn tính là đang tương tác đúng câu hỏi, chỉ thiếu nội dung.
- `NGOÀI_PHẠM_VI` thu hẹp lại: CHỈ áp dụng khi học viên **chủ động nêu tên một khái niệm/kỹ thuật cụ thể khác** (fine-tune, RLHF, temperature, attention, knowledge cutoff...).
- `ĐỦ_CĂN_CỨ` thêm yêu cầu self-consistency: agent phải có thể trích câu/cụm từ cụ thể khớp với từng tiêu chí trước khi tính là "matched" — không tin thẳng cảm giác tổng quát.

## 3. Bảng thống kê theo lớp chỗ khó — run-02 (số liệu chính thức)

| Lớp | Số case | Đạt | Tỷ lệ |
|---|---|---|---|
| ① Nguồn sự thật (`kho1_nguon_su_that`) | 2 | 0 | 0% |
| ② Mơ hồ/thiếu thông tin (`kho2_mo_ho`) | 3 | 3 | 100% |
| ③ Ngoài phạm vi/thẩm quyền (`kho3_ngoai_pham_vi`) | 3 | 3 | 100% |
| ④ Đặc thù nghiệp vụ (`kho4_dac_thu`) | 3 | 3 | 100% |
| Phổ biến hàng ngày (`common`) | 10 | 8 | 80% |
| Hiếm gặp (`edge`) | 4 | 4 | 100% |
| **Tổng** | **25** | **21** | **84,0%** |

Lớp ③ và ④ — hai lớp bị lỗi nặng nhất ở run-01 (0/3 và 33,3%) — sau khi sửa prompt đạt **100%** ở run-02. Đây là bằng chứng trực tiếp cho thấy nguyên nhân gốc đã xác định đúng.

## 4. Phân tích 4 case còn thất bại ở run-02

### 4.1 Lớp ① "Nguồn sự thật" — vẫn 0/2, ranh giới khó nhất còn tồn đọng (G01, G02)

- **G01** ("LLM bịa vì temperature đặt cao...") — giải thích đúng về mặt kỹ thuật, nhưng không thuộc 4 đoạn `[T06-138]`–`[T06-149]`. Agent trả `THIẾU_CĂN_CỨ` với rationale "chỉ nêu temperature, không đề cập 3 tiêu chí" — về hành vi (không công nhận đã hiểu) là an toàn, nhưng nhãn không khớp `NGOÀI_PHẠM_VI` nhóm kỳ vọng.
- **G02** ("cơ chế attention...") — lần này lỗi do agent **gọi tool vượt quá 4 vòng** (`MINILAB_MAX_TOOL_HOPS=4`), buộc `core.py` fallback về `THIẾU_CĂN_CỨ` mặc định trước khi mô hình kịp ra quyết định thật.

**Nhận định:** lớp ① là lớp khó nhất trong 4 lớp vì ranh giới giữa "nói đúng nhưng ngoài phạm vi" và "nói sai/thiếu trong phạm vi" phụ thuộc vào việc mô hình có nhận diện được thuật ngữ đó có tồn tại thật trong domain LLM nói chung hay không, dù nó không nằm trong 4 đoạn nguồn — đây vốn là rủi ro đã được `spec.md` §5 cảnh báo trước (transcript là văn nói, so khớp ngữ nghĩa khó hơn so khớp từ khoá). Về mặt sư phạm, cả hai case đều KHÔNG công nhận nhầm là đã hiểu (không phải lỗi đắt nhất), nên rủi ro thực tế thấp hơn nhóm lỗi B ở run-01.

### 4.2 Lớp "common" — 1 case false-positive còn sót (G14)

- **G14** ("Nó dự đoán token tiếp theo theo xác suất nên nghe câu trả lời rất trôi chảy") — chỉ chạm **c1** và **c3**, thiếu **c2** (vì sao vẫn trả lời khi thiếu dữ liệu), nhưng agent vẫn chấm `ĐỦ_CĂN_CỨ`.

Đây vẫn là loại lỗi **đắt nhất** theo nguyên tắc "chi phí lỗi không đối xứng" trong system prompt — dù đã thêm yêu cầu self-consistency ở run-02, `gpt-4o-mini` đôi lúc vẫn bỏ sót một tiêu chí khi câu trả lời của học viên "nghe" đủ ý nhưng thực chất thiếu một chân. Yêu cầu bằng văn bản trong prompt (nêu ra trong lời nhắc) không đủ chặt để triệt tiêu hoàn toàn lỗi này — cần một bước xác minh **có cấu trúc**, không chỉ dựa vào việc "nhắc" mô hình cẩn thận hơn.

### 4.3 Case G17 đổi loại lỗi nhưng chưa đạt (từ đúng ở run-01 sang sai ở run-02)

- **G17** ("Sao model được huấn luyện xong rồi mà vẫn không cập nhật được kiến thức mới") — ĐẠT ở run-01 nhưng FAIL ở run-02: agent giờ trả `THIẾU_CĂN_CỨ` với lý do "chỉ chạm c2, chưa đủ" — một cách đọc khác của cùng một input (model không tra cứu → không tự cập nhật, có thể bị coi là liên quan lỏng đến c2). Đây là **sự đánh đổi có thể lường trước**: khi thu hẹp định nghĩa `NGOÀI_PHẠM_VI` để sửa 7 case ở nhóm A, ranh giới với các câu hỏi "gần giống nhưng khác chủ đề" (như knowledge cutoff) cũng bị thu hẹp theo, khiến mô hình dễ cố gán một phần liên quan hơn là từ chối thẳng. Việc pass_rate tổng vẫn tăng mạnh (56%→84%) cho thấy đánh đổi này có lợi ròng, nhưng ranh giới lớp ① cần một vòng tinh chỉnh riêng (run-03) nếu còn thời gian.

## 5. Không có case nào agent bịa mã đoạn nguồn (cả hai lượt)

Kiểm tra điều kiện (3) của tiêu chí ĐẠT — không case nào trong 50 lượt chấm (25 case × 2 lượt) bị đánh fail do `source_id` không hợp lệ. Cơ chế tool-calling bắt buộc gọi `get_excerpt`/`list_scope` trước khi trích mã (theo thiết kế `agent/tools.py`) hoạt động đúng thiết kế.

## 7. Ghi chú về tính không ổn định (non-determinism) của LLM

Chạy thêm một lượt run-03 (tăng `MINILAB_MAX_TOOL_HOPS` từ 4 lên 6, không đổi gì khác) để kiểm tra đề xuất ở mục 6.3: kết quả vẫn **84,0% (21/25)** — xem [`eval/run_results_raw_v3.json`](run_results_raw_v3.json) — nhưng case fail đổi khác: G01 chuyển từ `THIẾU_CĂN_CỨ` (run-02) sang `ĐỦ_CĂN_CỨ` (run-03, false-positive), trong khi G02 vẫn fail nhưng giờ ra `THIẾU_CĂN_CỨ` thay vì bị cắt ngang giữa tool-call như run-02. Vì `temperature=0.2` không bằng 0, agent không đảm bảo trả lời giống nhau 100% giữa các lượt gọi ở ranh giới khó (lớp ① nguồn sự thật) — pass rate tổng ổn định quanh 84%, nhưng case cụ thể nào fail có thể xê dịch. Đây là hạn chế cần nêu rõ khi báo cáo: **84% là ước lượng, không phải số cố định tuyệt đối**, và lớp ① vẫn là lớp rủi ro nhất cần few-shot example trước CP4/CP5 nếu còn thời gian.

## 8. Kết luận & đề xuất cải thiện tiếp (nếu còn thời gian trước CP4)

- **Tỷ lệ đạt cuối cùng dùng để báo cáo: 84,0% (21/25)** với `gpt-4o-mini` qua OpenRouter, sau một vòng sửa prompt dựa trên số liệu thật của run-01. Đây là số liệu chưa chỉnh sửa, giữ nguyên cả case fail — theo đúng nguyên tắc "số xấu vẫn được đủ điểm, miễn số thật" của rubric CP3.
- Việc sửa **một đoạn prompt duy nhất** (làm rõ ranh giới `NGOÀI_PHẠM_VI` vs `THIẾU_CĂN_CỨ`) đã kéo pass rate tăng 28 điểm phần trăm — cho thấy phần lớn lỗi ban đầu là lỗi **định nghĩa mơ hồ trong prompt**, không phải lỗi năng lực mô hình.
- Lỗi còn tồn đọng ưu tiên sửa tiếp:
  1. **False-positive ĐỦ_CĂN_CỨ (G14)** — nguy hiểm nhất, cần chuyển từ "nhắc trong prompt" sang cơ chế có cấu trúc: ví dụ bắt buộc field `matched_criteria` phải kèm theo field mới `evidence_quote` (câu trích dẫn của học viên) cho mỗi tiêu chí, rồi validate ở code Python rằng quote đó thực sự xuất hiện trong input trước khi tin `matched_criteria`.
  2. **Ranh giới lớp ① "nguồn sự thật"** (G01, G02) — cần thêm ví dụ few-shot ngay trong prompt (một cặp input/output mẫu cho đúng loại "đúng kỹ thuật nhưng ngoài 4 đoạn") vì chỉ mô tả bằng lời chưa đủ phân biệt.
  3. **Tăng `MINILAB_MAX_TOOL_HOPS`** từ 4 lên 6-8 để tránh agent bị cắt ngang giữa lúc đang gọi tool xác minh (nguyên nhân của G02).
