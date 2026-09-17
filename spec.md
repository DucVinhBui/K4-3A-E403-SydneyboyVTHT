# AI SPEC — Agent học trò: học bằng cách dạy lại · Nhóm SydneyboyVTHT · Lớp 3A · Phòng E403

**Track:** D — Học tập thích ứng & tương tác trên VLearn · **Đề:** D3 — Học bằng cách dạy
**Loại:** Tính năng mới
**Trạng thái:** bản **CP4 — bản chốt spec**, nộp tại mốc 21:00 ngày 17/9/2026.
Quality bar ở **§7** khoá từ thời điểm này và không sửa sau đó.
Phần chưa làm xong được tự khai đầy đủ ở **§10**, kể cả phần bất lợi cho nhóm.

---

# CANVAS CP1 — 4 ô

## 01 · NGƯỜI DÙNG & NỖI ĐAU

### Học viên tưởng đã hiểu, nhưng không có gì kiểm chứng

**Job:** học viên khoá 4 vừa học xong một khái niệm trên VLearn (bài Foundation — transformer & attention), cần xác nhận mình đã thật sự hiểu trước khi đi tiếp.

**Pain:** căn cứ duy nhất để kết luận "mình hiểu rồi" là cảm giác đọc trôi. Trong 3.097 lượt hỏi-đáp của khoá, **99,81% lượt không ghi nhận mức hiểu nào** và chỉ **1 lượt (0,03%)** có ai chủ động hỏi ngược lại người học. Lỗ hổng chỉ lộ ra khi làm bài hoặc bị hỏi — lúc đó đã học sai sang các bài sau.

## 02 · BẰNG CHỨNG BAN ĐẦU

### Mining chatlog khoá 4, khảo sát lớp đang chạy

Mining `data/vlearn-pack/chatlog/tutor_turns.csv` (13.494 lượt, lọc `cohort_hint == "K4"` còn 3.097 lượt): phương pháp đếm kiểm lại được, số liệu ALL vs K4, và 5 trích dẫn nguyên văn dẫn `turn_id` — chi tiết trong [`evidence/mining-log.md`](evidence/mining-log.md).

Song song: khảo sát chuẩn A 6 câu đang thu, định nghĩa "một người xác nhận" đã chốt **trước** khi phát form — [`evidence/survey-questions.md`](evidence/survey-questions.md).

> 🔵 Không copy số liệu thô, snippet hay đoạn dài từ `data/` ra ngoài. Repo nộp chỉ chứa **số đếm và mã `turn_id`**, không chứa data pack.

## 03 · LÁT CẮT & AUTOMATION

### Một lời giải thích, một quyết định hỏi ngược

`ĐỦ_CĂN_CỨ`  `THIẾU_CĂN_CỨ`  `NGOÀI_PHẠM_VI`

Một học viên K4 vừa học xong đoạn "vì sao LLM bịa" **cần** giải thích lại khái niệm đó bằng lời của mình, **được** một agent học trò đối chiếu lời giải thích với bốn đoạn `[T06-136]`, `[T06-138]`, `[T06-139]`, `[T06-148]` và quyết định hỏi ngược đúng 2 câu tại chỗ thiếu căn cứ, **giúp** học viên bổ sung được dẫn chứng còn thiếu và đạt mức "đã dạy được" theo tiêu chí công bố trước phiên.

> 🟣 **Augment:** agent không tự chốt "đã hiểu". Hỏi ngược lạc chỗ thì học viên bỏ qua được, sửa rẻ; nhưng **công nhận nhầm một lời giải thích sai** thì học viên rời đi với kiến thức sai và không tự phát hiện được. Nên đoạn nguồn `[T06-xxx]` luôn hiện cạnh câu hỏi để học viên tự kiểm.

## 04 · NGƯỜI THỬ & PHÂN CÔNG

### Sáu người thử, bốn phần việc có tên

**Willing users dự kiến:** mời **≥6 người ngoài nhóm** thử prototype trước CP5. Track D bắt buộc ≥5 người *thực sự học một đoạn* bằng prototype, không chỉ bấm thử giao diện — nên mời dư để phòng người bận.

> 🟠 **4 vai trò:** spec + điều phối (Bùi Đức Vinh, đội trưởng) · evidence + mining (Đinh Công Tú) · prompt + eval (Đỗ Phúc Hưng) · build + demo (Bùi Đức Thông). Chi tiết: [`teammates.md`](teammates.md).

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

### Evidence — chuẩn B (mining) + kết quả chuẩn A (khảo sát không đạt ngưỡng)

Log đầy đủ + phương pháp đếm kiểm lại được: **[`evidence/mining-log.md`](evidence/mining-log.md)**

| Số liệu | ALL (n=13.494) | K4 (n=3.097) |
|---|---|---|
| Không ghi nhận mức hiểu (`understanding_level` rỗng) | 99,85% | **99,81%** |
| Có hỏi ngược người học (`ask_probing_question`) | 28 (0,21%) | 6 (0,19%) |
| **Chủ động** kiểm tra hiểu (đọc nguyên văn 6 lượt K4) | — | **1 lượt (0,03%)** |
| Có phản hồi của người học (`rating`) | 1,31% | 0,39% |
| Độ dài trả lời / câu hỏi | 6,8× | **6,4×** |

Năm ví dụ nguyên văn kèm `turn_id`: `T10296` · `T10300` · `T10970` · `T10939` · `T10507` — xem `evidence/mining-log.md` §4.

#### Chuẩn A — đã chốt kết quả

Bộ câu hỏi: **[`evidence/survey-questions.md`](evidence/survey-questions.md)** · Log kết quả: **[`evidence/survey-log.md`](evidence/survey-log.md)**

**Định nghĩa "một người xác nhận" — chốt trước khi phát form, không sửa sau:** người trả lời thoả CẢ HAI: **(a)** ở Câu 2 chọn *"Thấy quen, đọc trôi được"* hoặc *"Đọc lại thấy ổn"* (căn cứ duy nhất là cảm giác, không có bằng chứng bên ngoài), **VÀ (b)** ở Câu 3 chọn *"Có — tôi kể lại được lần đó"* (đã thật sự hiểu sai sau khi tưởng đã hiểu).

**Ngưỡng đạt:** n ≥ 20 người ngoài nhóm và tỉ lệ xác nhận > 50%.

**Bộ câu hỏi có thể fail:** người chọn *"Tự làm được bài tập"* hoặc *"Giải thích lại được cho người khác"* ở C2 là người **không** xác nhận. Không đổi định nghĩa sau khi xem dữ liệu.

| | n | Xác nhận | Tỉ lệ | Đạt? |
|---|---|---|---|---|
| Kết quả | **20** | **2** | **10%** | **Không đạt** |

Kết quả chuẩn A không xác nhận giả định mạnh rằng hơn một nửa học viên vừa dựa vào cảm giác đọc trôi/đọc lại thấy ổn, vừa kể lại được một lần họ đã hiểu sai. Tuy vậy, dữ liệu vẫn cho hai tín hiệu hẹp hơn: **11/20** người dùng dấu hiệu yếu ở C2 và **18/20** nói từng phát hiện mình hiểu sai ở C3. Vì vậy nhóm không dùng khảo sát để tuyên bố pain point đã được đa số xác nhận; nhóm giữ lát cắt D3 dựa trên bằng chứng hành vi chuẩn B và thu hẹp phát biểu thành: **luồng học hiện tại thiếu một bước kiểm tra ngay tại chỗ buộc học viên giải thích bằng lời của mình trước khi đi tiếp.**

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
3. **Nguồn đối chiếu đã có sẵn, không phải dựng**: `transcript-06-clean.md` có 162 mã đoạn để trích dẫn. Sau khi kiểm tra nguyên văn, bốn đoạn dùng để chấm là `[T06-136]` (dự đoán token), `[T06-138]` và `[T06-139]` (bias), `[T06-148]` (knowledge cutoff). *(Đây là bộ mã đã xác minh trên transcript thật; stack Python đang chạy bản mẫu vẫn dùng một bộ mã fixture khác — xem §3.)*

---

## §3. Dữ liệu & nguồn sự thật

> *Mục này được dựng ở CP4. Bản CP1/CP2 nhảy thẳng từ §2 sang §4 — spec thiếu hẳn phần khai nguồn dữ liệu, trong khi toàn bộ sản phẩm là một cỗ máy đối chiếu. Nhóm không còn file `03-ai-spec-template.md` trên máy nên đặt tên mục theo đúng thứ nó phải trả lời; nếu template gốc đặt tên khác thì đổi tiêu đề, nội dung giữ nguyên.*

### Ba nguồn, ba mục đích, và cái nào được phép nằm trong repo

| Nguồn | Dùng vào việc gì | Nằm ở đâu | Commit lên repo public? |
|---|---|---|---|
| `data/vlearn-pack/chatlog/tutor_turns.csv` — 13.494 lượt, lọc `cohort_hint == "K4"` còn 3.097 | Bằng chứng chuẩn B ở §1–§2 (99,81% · 0,03%) | Máy cá nhân, **ngoài** repo | **Không.** Repo chỉ chứa **số đếm** và mã `turn_id` để kiểm lại |
| `data/vlearn-pack/transcript/transcript-06-clean.md` — 162 mã đoạn `[T06-NNN]` | Nguồn đối chiếu lời giải thích của học viên | `codebase/prototype/sources.local.json` — nằm trong `.gitignore` | **Không.** Repo chỉ chứa **mã đoạn**, không chứa nguyên văn |
| Khảo sát chuẩn A, n = 20 | Kiểm giả định pain point ở §1 | [`evidence/survey-log.md`](evidence/survey-log.md) | **Có** — dữ liệu của lớp, đã ẩn danh |

`.gitignore` chặn sẵn `data/`, `*.csv`, `vlearn-pack/`, `**/sources.local.json` và `.env`. Đây là ràng buộc bắt buộc: repo nộp bài đang **public**, còn data pack là tài liệu nội bộ của khoá.

### Agent được cấp đúng bốn đoạn — và hiện có hai danh sách khác nhau

Agent **chỉ** được đọc bốn đoạn. Ngoài bốn đoạn đó, nó phải trả `NGOÀI_PHẠM_VI` chứ không được suy diễn. Nhưng tại CP4, hai stack trong repo đang cầm hai bộ mã đoạn khác nhau:

| | Stack Python *(bản mẫu đang chạy)* | Stack Node |
|---|---|---|
| Bốn mã đoạn | `[T06-138]` `[T06-141]` `[T06-145]` `[T06-149]` | `[T06-136]` `[T06-138]` `[T06-139]` `[T06-148]` |
| Nội dung | ⚠️ **fixture nhóm tự viết** — `codebase/knowledge/hallucination.json`, trường `source_label` ghi rõ `MOCK` | ✅ **nguyên văn transcript thật**, nạp từ `sources.local.json` |
| Đã đối chiếu với transcript thật chưa | **Chưa.** Bốn mã này đặt ra ở CP2 khi data pack không còn trên máy | **Rồi** — mã và nội dung đã kiểm lại từng đoạn |

Hai danh sách chỉ trùng nhau đúng một mã (`T06-138`). Nhóm khai thẳng chỗ này thay vì chọn một bên rồi im lặng — chi tiết cách xử lý ở §7 và §10.

### Nguồn đối chiếu là dữ liệu tách rời, không phải chữ trong code

Từ CP3, nguồn đối chiếu nằm trong [`codebase/knowledge/`](codebase/knowledge/) dưới dạng **pack JSON**, chọn bằng biến môi trường `MINILAB_TOPIC`. Mỗi pack khai đủ: khái niệm, phạm vi, nhãn nguồn, 4 đoạn có mã, 3 tiêu chí *(mỗi tiêu chí trỏ về đúng một mã đoạn)*, câu hỏi đào sâu, và danh sách khái niệm cố tình để ngoài phạm vi.

Có 5 pack: `hallucination` *(mặc định — khái niệm của lát cắt)*, `toolcall`, `grounding`, `eval-first`, `automation-level`. Bốn pack sau không phải để mở rộng sản phẩm — chúng tồn tại để **kiểm chứng rằng agent bám vào nguồn được cấp chứ không bám vào kiến thức nền của LLM**: cùng một bộ ca chạy qua cả 5 pack phải ra cùng một kiểu hành vi (§7, bộ đo thứ ba).

`agent/sources.py` từ chối nạp pack hỏng ngay lúc khởi động — trùng mã đoạn, tiêu chí trỏ vào mã không tồn tại, hoặc `name` lệch tên file đều ném lỗi. Thà chết lúc khởi động còn hơn để agent đi đối chiếu với nguồn rác.

### Dữ liệu người dùng — chưa có

Sản phẩm **không lưu** bài của học viên ra đâu cả: log phiên sống trong bộ nhớ trang, đóng tab là mất, không dùng `localStorage`. File `codebase/logs/llm_calls.jsonl` ghi vết từng lời gọi LLM để kiểm chứng số đo, nằm trong `.gitignore`, không commit.

Vòng validation ở CP5 sẽ là lần đầu có dữ liệu người thật — sẽ nằm trong `validation/` và chỉ lưu quote nguyên văn kèm tên người đã đồng ý cho thử, không lưu gì thêm.

---

## §4. Thiết kế

### Lát cắt MỘT CÂU
> Một học viên K4 vừa học xong đoạn "vì sao LLM bịa" **cần** giải thích lại khái niệm đó bằng lời của mình, **được** một agent học trò đối chiếu lời giải thích với bốn đoạn `[T06-136]`, `[T06-138]`, `[T06-139]`, `[T06-148]` và quyết định hỏi ngược đúng 2 câu tại chỗ thiếu căn cứ, **giúp** học viên bổ sung được dẫn chứng còn thiếu và đạt mức "đã dạy được" theo tiêu chí công bố trước phiên.

*Bốn mã đoạn trên là bộ đã xác minh trên transcript thật. Stack đang chạy bản mẫu vẫn dùng fixture với bộ mã khác — khai đầy đủ ở §3 và §10, mục 6.*

### Non-goals — những thứ KHÔNG build
1. **Không chấm điểm học viên.** Đây là chỗ luyện, không phải chỗ thi — không có điểm số nào được ghi lại hay báo về giảng viên dưới dạng đánh giá.
2. **Chỉ một bài giảng** (`transcript-06`) và **một khái niệm** ("vì sao LLM bịa"). Không đa bài, không đa khái niệm.
3. **Không có persona thay đổi theo lịch sử học viên.** Agent học trò có một mức hiểu cố định, công bố trước.
4. **Không đa tác tử.** Đúng một vai agent.

### Mức prototype nhắm tới
**Working (thu hẹp phạm vi)** — đích ở CP3/CP5: agent gọi thật, đối chiếu thật với đoạn transcript có mã.

**Bản mẫu:** [`codebase/prototype/index.html`](codebase/prototype/index.html) — một file HTML tự chứa, mở bằng `file://` là chạy, không cần mạng. Bốn màn M1→M4, bấm đi hết được cả 4 nhánh trải nghiệm (§6).

Cùng file còn có **sơ đồ luồng** (nút *⤳ Sơ đồ luồng* trên thanh tiêu đề): vẽ rõ điểm nhập liệu, hai cổng chặn trước, **điểm gọi quyết định AI** `decide()`, ba nhánh đi ra và hai nhánh ngoại lệ — đáp ứng luôn hình thức flowchart mà mốc CP2 chấp nhận.

| Thành phần | Trạng thái tại **CP4** | Còn nợ gì |
|---|---|---|
| Luồng 4 màn, điều hướng, log phiên | **thật** từ CP2 | — |
| Panel đoạn nguồn `[T06-xxx]` luôn hiện cạnh câu hỏi | **thật** từ CP2 | — |
| Nút *Không đồng ý với đánh giá này* ở mọi màn M3 | **thật** từ CP2 | — |
| **Quyết định chọn trạng thái** (`ĐỦ_CĂN_CỨ` / `THIẾU_CĂN_CỨ` / `NGOÀI_PHẠM_VI`) | **thật** — `agent/core.py` gọi LLM (`gpt-4o-mini`, OpenAI) qua vòng tool-calling, output ép theo JSON schema. Heuristic đếm từ khoá của CP2 đã bị gỡ bỏ | Ranh giới lớp ① còn 1 ca trượt (`G02`, xem §5 dòng 2) |
| Tiêu chí "đã dạy được" | **thật** — LLM tự khai `matched_criteria`, nhưng **Python kiểm lại**: mỗi tiêu chí phải kèm `matched_evidence` là câu nguyên văn của học viên và câu đó phải thật sự nằm trong bài, nếu không thì tiêu chí bị loại và hạ trạng thái. Ngưỡng cứng 3/3 của CP2 đã bị gỡ | — |
| Hỏi ngược đúng 2 câu, mỗi câu gắn mã đoạn | **thật** — `_ensure_probes()` bảo đảm đúng 2 câu; `_fix_probe_citations()` sửa mã đoạn rỗng/bịa trước khi trả về | — |
| **Nội dung 4 đoạn nguồn** | ⚠️ **vẫn MOCK trên stack chính** — fixture nhóm tự viết trong `codebase/knowledge/hallucination.json`, gắn nhãn `MOCK` ngay trên UI | Đọc từ `transcript-06-clean.md` thật. Stack Node đã làm được việc này (xem §3 và §7) |

> **Vì sao đoạn nguồn ở CP2 là fixture tự viết, không phải transcript thật:** data pack của khoá là tài liệu nội bộ và repo nộp bài đang **public**. Nhóm không đưa nội dung transcript vào file commit; bản mẫu chỉ dùng **mã đoạn** `[T06-xxx]` và fixture tự viết có nhãn `MOCK`.

### Automation: **augment**
Lý do theo cost-of-error: quyết định đắt nhất **không phải** "hỏi ngược sai chỗ" — học viên thấy câu hỏi lạc thì bỏ qua được, sửa rẻ. Đắt nhất là agent **công nhận "đã hiểu" cho một lời giải thích sai**: học viên rời đi với kiến thức sai và **không tự phát hiện được**, sai lan sang các bài sau. Nên agent không tự chốt: đoạn `[T06-xxx]` gốc luôn hiển thị cạnh câu hỏi để học viên tự đối chiếu, và học viên luôn xem được mình bị đánh giá thiếu ở đâu.

### §4b. Bốn nguyên tắc HAX/PAIR — vị trí áp dụng chính xác trong bản mẫu

| Nguyên tắc | Màn | Thành phần cụ thể trong `codebase/prototype/index.html` |
|---|---|---|
| **G2** — Làm rõ nó làm tốt đến đâu | **M1** | Khối *"Phạm vi — mình chỉ đối chiếu được đúng chừng này"* và *"Tiêu chí đã dạy được"*: ba tiêu chí được đánh số kèm mã đoạn, in ra **trước** khi học viên gõ chữ nào, và M4 kết luận đúng theo ba tiêu chí đó chứ không theo tiêu chí khác |
| **G10** — Thu hẹp phạm vi khi nghi ngờ *(bắt buộc)* | **M3**, nhánh `NGOÀI_PHẠM_VI` | Câu *"Bốn đoạn của mình không có chỗ nào nói về cái đó, nên mình **không nói bạn đúng hay sai**"* — bốn mã đoạn cụ thể do pack đang chạy quyết định, bản mẫu nạp qua `GET /api/scope` (xem §3) — agent từ chối phán xét thay vì đoán bừa |
| **G11** — Giải thích vì sao | **M3**, mọi câu hỏi ngược | Dòng `mình dựa vào [T06-138] — bấm để xem` ngay dưới **mỗi** câu hỏi; bấm vào là đoạn đó sáng lên trong panel nguồn bên phải |
| **G9** — Sửa dễ dàng | **M3 → M2** | Nút *"Bổ sung — giữ nguyên bài mình đã viết"*: quay lại M2 **không xoá** nội dung cũ, kèm banner nhắc là bổ sung chứ không gõ lại. Cộng thêm nút *"Không đồng ý với đánh giá này"* có mặt ở **mọi** màn M3 |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + 10 kịch bản

Rủi ro lớn nhất đã xác định từ CP1: transcript là **văn nói** (ẩn dụ, ngắt câu tự nhiên), nên so khớp lời giải thích bằng keyword/regex sẽ vỡ ngay ở trường hợp *"học viên giải thích đúng nhưng khác cách diễn đạt tài liệu"*. Phải đối chiếu ngữ nghĩa, không phải so chuỗi. Toàn bộ thiết kế ở §4 đi theo kết luận này.

### 4 lớp chỗ khó

| Lớp | Tình huống | Hành vi mong muốn |
|---|---|---|
| ① Nguồn sự thật | Học viên nói một ý **đúng** nhưng không có trong bốn đoạn được cấp | Nói rõ "ngoài phạm vi đoạn đang học", không phán đúng/sai |
| ② Mơ hồ | Học viên chỉ gõ một dòng ngắn, không đủ để đánh giá | Hỏi lại để lấy thêm, không kết luận |
| ③ Ngoài phạm vi / thẩm quyền | Học viên đòi đáp án, đòi làm hộ bài | Từ chối đưa đáp án, đưa lại đoạn nguồn để tự đọc |
| ④ Đặc thù domain | Học viên giải thích **sai nhưng rất tự tin** | Không công nhận "đã hiểu"; hỏi ngược đúng chỗ sai, kèm mã đoạn |

### 10 kịch bản — mỗi kịch bản là một ca đo được

Bảng dưới **không phải kịch bản tưởng tượng**. Mỗi dòng là một ca có thật trong [`codebase/eval/golden_set.json`](codebase/eval/golden_set.json) hoặc [`codebase/eval/kb_cases.json`](codebase/eval/kb_cases.json), đã chạy qua LLM thật. Cột cuối là **hành vi thực đo** ở lượt chính thức run-04 (§7), không phải kỳ vọng.

| # | Lớp | Học viên gõ gì | Hành vi mong muốn | Thực đo |
|---|---|---|---|---|
| 1 | ① | *"LLM bịa vì **temperature** đặt cao…"* — `G01` | `NGOÀI_PHẠM_VI`: đúng về kỹ thuật nhưng không nằm trong bốn đoạn được cấp, nên không phán đúng/sai | ✅ đạt sau khi liệt kê tên các khái niệm ngoài phạm vi vào prompt |
| 2 | ① | *"Mình nghĩ là do cơ chế **attention**…"* — `G02` | `NGOÀI_PHẠM_VI` | ❌ ra `THIẾU_CĂN_CỨ` — **ca duy nhất còn trượt**. "Attention" nghe gần với "cơ chế sinh token" nên agent cố gán một phần liên quan thay vì từ chối thẳng |
| 3 | ② | *"hmm"* · *"Chắc là do lỗi gì đó thôi?"* — `G03` `G04` `G05` | `THIẾU_CĂN_CỨ`, hỏi ngược đúng 2 câu, không kết luận | ✅ 3/3 |
| 4 | ② | Gõ bừa: *"dsfkj alksdjf laksjdf…"* — `G22` | `THIẾU_CĂN_CỨ` — **không** phải `NGOÀI_PHẠM_VI`: không gọi tên được chủ đề nào khác thì không có gì để nói là "ngoài phạm vi" | ✅ |
| 5 | ③ | *"Cho mình đáp án luôn đi"* · *"Làm hộ mình bài quiz"* — `G06` `G07` `G08` | `THIẾU_CĂN_CỨ`: từ chối đưa đáp án, trả về đoạn nguồn. Vẫn tính là học viên đang ở đúng bài | ✅ 3/3 |
| 6 | ③ | *"mỳ cay ngon"* — 11 ký tự — `OFF-01` | `NGOÀI_PHẠM_VI`: chủ đề khác hẳn, **kể cả khi bài rất ngắn** | ✅ — từng sai, xem §9 dòng *bỏ cổng <40 ký tự* |
| 7 | ④ | *"nó **lười** tính toán"* · *"nó có **cảm xúc**"* · *"**RAM đầy**"* · *"**server lag**"* — `G09` `G10` `G11` `G23` | `THIẾU_CĂN_CỨ`: sai bét nhưng **vẫn đang trả lời đúng câu hỏi**, nên hỏi ngược chứ không đẩy ra ngoài phạm vi | ✅ 4/4 — từng trượt cả nhóm này ở lượt 64%, xem §7 |
| 8 | ④ · **lỗi đắt nhất** | *"Nó dự đoán token theo xác suất nên nghe rất trôi chảy"* — chạm c1 và c3, thiếu c2 — `G14` | `THIẾU_CĂN_CỨ`: **không** được công nhận là đã hiểu | ✅ sau khi thêm `matched_evidence` + kiểm bằng Python. Trước đó đây là false-positive, và rationale của agent nghe rất thuyết phục |
| 9 | Hard test riêng của đề D3 | Dán nguyên văn đoạn nguồn rồi bấm gửi — `G16` `G24` | `THIẾU_CĂN_CỨ` + gọi tên đúng hành vi: *"chỗ này là chữ của tài liệu, chưa phải chữ của bạn"* | ✅ 2/2. Cờ `is_verbatim_paste` **chỉ** do cổng deterministic đặt, không nhận giá trị LLM tự khai |
| 10 | Bất biến xuyên mọi lớp | Bất kỳ input nào | Mọi `source_id` agent trích ra phải là mã **có thật** trong nguồn được cấp — không bịa mã đoạn | ✅ 0/50 lượt golden set · 0/45 ca knowledge base |

### Vì sao ba dòng cuối tách riêng

Dòng 8, 9, 10 không phải viết thêm cho đủ số. Chúng là ba lớp lỗi mà **kiểm bằng mắt không bắt được**:

- **Dòng 8** là lỗi đắt nhất theo chính §4. Nó nguy hiểm vì không tự mâu thuẫn: agent khai khớp đủ ba tiêu chí kèm một lý do mạch lạc, đọc qua không thấy sai. Chỉ khi bắt nó trích nguyên văn chữ học viên rồi dò lại bằng Python mới lộ.
- **Dòng 9** là hard test riêng của đề D3: dán tài liệu là cách rẻ nhất để "qua bài" mà không học gì. Nếu agent khen bài dán là đã hiểu thì sản phẩm phản tác dụng chứ không phải vô hại.
- **Dòng 10** là loại lỗi người chấm không thể tự kiểm trong 30 giây xem demo — một mã đoạn bịa nhìn y hệt một mã đoạn thật. Phải để máy kiểm, và phải kiểm trên mọi ca.

### Hai chỗ đã sửa nhờ bảng này

1. **Dòng 6 từng sai.** `core.py` có cổng cứng `len(text) < 40 → THIẾU_CĂN_CỨ` chạy **trước** LLM, nên *"mỳ cay ngon"* bị xếp thành "chưa đủ nội dung" thay vì "nói chuyện khác". Đếm ký tự không phân biệt được hai thứ đó. Đã gỡ cổng, chuyển phân loại vào prompt.
2. **Dòng 7 từng kéo cả bộ đo xuống.** Bản sửa đầu tiên của cổng lĩnh vực bắt quá tay, ném luôn nhóm "sai nhưng đúng bài" sang `NGOÀI_PHẠM_VI`. Golden set tụt còn 64%. Ranh giới đúng phải là ba tầng, không phải hai:

| Học viên viết gì | Trạng thái | Vì sao |
|---|---|---|
| Chủ đề khác hẳn, gọi tên được (mỳ cay, bóng đá) | `NGOÀI_PHẠM_VI` | Agent không có căn cứ, không phán đúng/sai |
| Khái niệm AI có thật nhưng ngoài bốn đoạn (temperature, attention, RLHF) | `NGOÀI_PHẠM_VI` | Có thật trong ngành, ngoài phạm vi được cấp |
| Gõ bừa, hoặc sai bét nhưng vẫn đang trả lời đúng câu hỏi | `THIẾU_CĂN_CỨ` | Không có chủ đề khác để gọi tên |

---

## §6. Bốn đường đi của trải nghiệm

Cả bốn đều bấm đi hết được trong [`codebase/prototype/index.html`](codebase/prototype/index.html); bốn nút preset ở cuối màn M2 nạp sẵn câu trả lời mẫu để demo 5 phút không phụ thuộc gõ tay.

### ① Happy path — AI tự tin cao
- **Kích hoạt:** lời giải thích chạm đủ 3/3 tiêu chí công bố ở M1 → `ĐỦ_CĂN_CỨ`, mức tự tin *cao*
- **Agent làm gì:** công nhận **tạm**, và nói thẳng là nó **không tự chốt** — đẩy học viên sang panel nguồn để tự đối chiếu. Đây chính là chỗ mức *augment* thể hiện ra giao diện
- **Học viên đi tiếp:** *Mình đã đối chiếu — đúng rồi* → M4, ghi "đã dạy được" · *Chưa, mình muốn sửa lại* → M2
- **Ở đâu:** M3, `kind:"ok"`

### ② Low-confidence — AI thiếu tự tin
- **Kích hoạt:** chạm 1–2/3 tiêu chí → `THIẾU_CĂN_CỨ`, mức tự tin *thấp*. Hai biến thể cùng nhánh: bài **quá ngắn** (<40 ký tự, lớp ② mơ hồ ở §5) và **dán nguyên văn tài liệu** (hard test của đề D3)
- **Agent làm gì:** hỏi ngược **đúng 2 câu**, nhắm vào đúng tiêu chí còn hổng, mỗi câu gắn mã đoạn. **Không** đưa đáp án — và nói rõ với học viên là cố tình không đưa
- **Học viên đi tiếp:** *Bổ sung — giữ nguyên bài mình đã viết* → M2, nội dung cũ **không bị xoá** (G9)
- **Ở đâu:** M3, `kind:"gap" | "short" | "paste"`

### ③ Failure / no-grounding — không tìm thấy căn cứ
- **Kích hoạt:** không chạm tiêu chí nào, lại nói sang thứ không có trong 4 đoạn → `NGOÀI_PHẠM_VI`, cột tự tin đổi thành *"không đánh giá đúng/sai"*
- **Agent làm gì:** gọi tên đúng thứ học viên vừa nói, nói rõ nó **không có căn cứ để phán đúng/sai**, không đoán bừa (G10)
- **Học viên đi tiếp:** *Viết lại trong phạm vi* → M2 · *Cho mình xem phạm vi gồm những gì* → sáng đoạn nguồn
- **Ở đâu:** M3, `kind:"out"`

### ④ Correction — học viên can thiệp sửa kết quả
- **Kích hoạt:** nút *Không đồng ý với đánh giá này*, có mặt ở **mọi** màn M3 kể cả happy path
- **Agent làm gì:** mở form cho học viên nói agent sai chỗ nào **và** chọn lại trạng thái đúng ra phải là gì; ghi cả hai vào log phiên rồi hiện banner *"Đánh giá của mình ở trên không được dùng để kết luận nữa — bạn giữ quyền quyết định"*
- **Học viên đi tiếp:** ở lại M3, chọn đường nào cũng được; nút *Kết thúc phiên* luôn có nên không bao giờ tắc
- **Ở đâu:** M3, `#correct` + `#disagree`

**Không có đường cụt:** mọi màn M3 đều có *Kết thúc phiên* → M4, và M4 luôn có *Dạy lại lần nữa* / *Bắt đầu phiên mới*.

---

## §7. Kiểm thử

> **QUALITY BAR — KHOÁ 21:00 NGÀY 17/9/2026.**
> Bốn điều kiện và bốn ngưỡng dưới đây được chốt tại mốc CP4 và **không sửa sau mốc này**.
> Mọi lượt chạy về sau chỉ được cập nhật **giá trị đo được**, không được cập nhật ngưỡng.

### Thế nào là "đạt"

Sản phẩm gọi là **đạt** khi thoả **cả bốn** điều kiện. Ba điều kiện đầu đo trên golden set; điều kiện thứ tư đo trên người thật — ràng buộc riêng của track D.

| # | Điều kiện | Ngưỡng *(khoá)* | Đo được tại 17/9 |
|---|---|---|---|
| 1 | **Đúng trạng thái** — `decision.state` khớp `expected_state` trên golden set 25 ca | ≥ **80%** | **96,0%** — 24/25 ✅ |
| 2 | **Không bịa nguồn** — mọi `source_id` trong `probes` phải là mã có thật trong nguồn được cấp | **0 ca** vi phạm | 0/50 lượt golden + 0/45 ca KB ✅ |
| 3 | **Lỗi đắt nhất** — công nhận `ĐỦ_CĂN_CỨ` cho lời giải thích còn thiếu tiêu chí *(false-positive)* | ≤ **1/25** | **0/25** ✅ |
| 4 | **Chỉ số HỌC** *(bắt buộc của track D)* — tỉ lệ người thử bổ sung được **≥1 dẫn chứng còn thiếu** ngay trong phiên sau khi bị hỏi ngược | ≥ **60%**, n ≥ 5 | **chưa đo** ⛔ |

> **Kết luận tại CP4: đạt 3/4, chưa đo 1. Nhóm KHÔNG tuyên bố sản phẩm đã đạt quality bar.**
> Điều kiện 4 chỉ đo được ở vòng validation CP5, hiện chưa có người ngoài nhóm nào thử — xem §10.

**Vì sao điều kiện 3 tách riêng khỏi điều kiện 1:** vì **chi phí lỗi không đối xứng**. Hỏi ngược lạc chỗ thì học viên bỏ qua được, sửa rẻ; còn công nhận nhầm một lời giải thích sai thì học viên rời đi với kiến thức sai và **không tự phát hiện được**. Một bộ đạt 96% nhưng toàn lỗi loại false-positive vẫn là bộ **trượt**. Điều kiện 1 đo độ đúng trung bình, điều kiện 3 đo riêng loại lỗi đắt nhất — hai chuyện khác nhau.

### Số đo — hai stack, hai bộ đo, khai cả hai

Repo hiện có **hai** hệ thống chạy được, cả hai đều gọi LLM thật, và chúng cho hai con số khác nhau. Nhóm khai cả hai thay vì giấu một bộ:

| | **Bộ A — số chính thức** | Bộ B — độc lập |
|---|---|---|
| Stack | Python · `codebase/agent/` + `codebase/api/server.py` | Node · `codebase/server.mjs` |
| Bộ ca | [`codebase/eval/golden_set.json`](codebase/eval/golden_set.json) — **25 ca**, đủ taxonomy 4 lớp ở §5 | [`eval/cases.json`](eval/cases.json) — **20 ca** |
| Kết quả | **24/25 = 96,0%** · `gpt-4o-mini` qua OpenAI trực tiếp | **19/20 = 95%** · `gpt-4o-mini-2024-07-18` |
| Nguồn đối chiếu | ⚠️ **fixture MOCK** — `codebase/knowledge/hallucination.json` | ✅ **transcript thật** qua `sources.local.json` *(không commit)* |
| Ca trượt | `G02` — attention, lớp ① | `gap-06` — kỳ vọng `THIẾU_CĂN_CỨ`, ra `NGOÀI_PHẠM_VI` |
| Báo cáo | [`codebase/eval/run_results.md`](codebase/eval/run_results.md) | [`eval/cp3-measurement.md`](eval/cp3-measurement.md) |

**Vì sao bộ A là số chính thức:** bản mẫu mà học viên thật sự bấm — `codebase/prototype/index.html` — gọi `/api/config`, `/api/scope`, `/api/eval/cases`. Ba endpoint này **chỉ có trên stack Python**; stack Node phục vụ đúng `/api/decide`. Bộ A vì thế là bộ duy nhất đo đúng đoạn mã chạy trong video CP3 và trong buổi demo. Bộ A cũng là bộ có taxonomy 4 lớp chỗ khó, có log thô từng lời gọi LLM, và có cơ chế kiểm `matched_evidence`.

**Điểm mạnh của bộ B mà bộ A không có:** bộ B đối chiếu với **transcript thật**, bộ A vẫn đang đối chiếu với fixture do nhóm tự viết. Đây là khoản nợ đã khai ở §3 và §10, và là lý do con số 96% phải đọc kèm chú thích chứ không đọc trần.

### Bộ đo thứ ba — knowledge base

`python -m eval.run_kb_check` → **45 ca · 45 đạt · 100%** · kết quả [`codebase/eval/kb_check_results.json`](codebase/eval/kb_check_results.json).

Bộ này chạy 9 ca với **từng** pack trong `codebase/knowledge/` (5 pack × 9 ca): 6 ca dùng chung cho mọi pack (lạc đề, gõ bừa, sai-nhưng-đúng-bài, xin đáp án) và 3 ca riêng từng khái niệm (đủ ý / thiếu ý / khái niệm khác). Nó kiểm một bất biến mà golden set không kiểm: **mọi mã đoạn agent trích ra phải có thật trong pack đang chạy** — 0/45 ca trích mã bịa.

Mục đích của bộ này không phải mở rộng sản phẩm. Nó trả lời một câu hỏi khác: *agent đang bám vào nguồn được cấp, hay đang bám vào kiến thức nền của `gpt-4o-mini`?* Nếu đổi pack mà hành vi không đổi theo pack thì nguồn đối chiếu chỉ là đồ trang trí.

### Bốn lượt chạy — giữ nguyên cả lượt xấu

| Lượt | Kết quả | Đổi gì trước lượt đó |
|---|---|---|
| run-01 | 56,0% — 14/25 | Prompt gốc |
| run-02 | 84,0% — 21/25 | Làm rõ ranh giới `NGOÀI_PHẠM_VI` vs `THIẾU_CĂN_CỨ` sau khi đọc log run-01 |
| run-03 | 84,0% — 21/25 | Tăng `MINILAB_MAX_TOOL_HOPS` 4 → 6. Pass rate không đổi nhưng **ca trượt đổi khác** |
| **run-04** | **96,0% — 24/25** | Gỡ cổng <40 ký tự · thêm `matched_evidence` + kiểm bằng Python · cờ verbatim chỉ do code đặt |

Giữa run-03 và run-04 có **một lượt đi sai không đánh số: 64% — 16/25**, khi cổng lĩnh vực bắt quá tay và ném cả nhóm "sai nhưng đúng bài" ra `NGOÀI_PHẠM_VI` (§5, dòng 7). Bảy ca trượt cùng một kiểu. Nhóm giữ lượt này trong báo cáo thay vì xoá, vì nó là bằng chứng cho đúng công dụng của bộ đo khoá trước: **nếu chỉ thử tay vài câu lạc đề thì thay đổi đó trông hệt như một cải tiến.**

Không lượt nào được chạy lại riêng ca trượt để thay số. Ngưỡng ở bảng quality bar không đổi qua cả bốn lượt.

### Ba giới hạn phải khai khi báo cáo con số này

1. **96% là ước lượng, không phải hằng số.** `temperature = 0.2` nên ca trượt cụ thể xê dịch giữa các lượt — run-03 vẫn ra 84% nhưng đổi ca trượt. Lớp ① là lớp không ổn định nhất.
2. **Bộ A đo trên nguồn MOCK.** Phải chạy lại sau khi đặt transcript thật vào nguồn của stack Python trước khi dùng con số này cho bản nộp cuối.
3. **Điều kiện 4 chưa có một dòng dữ liệu nào.** Chưa có người ngoài nhóm nào dùng thử, nên phần "sản phẩm này có làm người ta học được không" hiện **chưa được kiểm chứng** — chỉ mới kiểm chứng được là agent hành xử đúng thiết kế.

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
| 16/9 · CP2 | Dựng bản mẫu tương tác HTML 4 nhánh trong `codebase/`; điền §6, viết lại §4b thành bảng có vị trí cụ thể | Mốc CP2 yêu cầu bản mẫu chạy thông + §4/§6 cập nhật. Đoạn nguồn dùng fixture tự viết vì repo nộp đang public và data pack là tài liệu nội bộ |
| 17/9 · CP3 | Cắm lời gọi LLM thật (OpenRouter · `openai/gpt-4o-mini`) vào `StateCheckAgent.decide()`, thêm cơ chế ghi vết `logs/llm_calls.jsonl` (prompt đầy đủ + response thô mỗi lượt gọi); xây `eval/golden_set.json` 25 case theo taxonomy 4 lớp; chạy 2 lượt (run-01 → sửa prompt → run-02), pass rate 56%→84% | Mốc CP3 bắt buộc ≥1 lời gọi AI thật ở mắt xích quyết định trung tâm + số đo thật. Sửa `NGOÀI_PHẠM_VI` vs `THIẾU_CĂN_CỨ` trong system prompt sau khi đọc log run-01 phát hiện model gộp hai điều kiện lại thành một |
| 17/9 · CP3 | **Khảo sát chuẩn A KHÔNG ĐẠT ngưỡng đã khoá: 2/20 = 10%, cần > 50%.** Giữ nguyên định nghĩa `a ∧ b`, không sửa sau khi xem dữ liệu. Thu hẹp phát biểu ở §1: không tuyên bố pain point đã được đa số xác nhận, giữ lát cắt D3 dựa trên bằng chứng hành vi chuẩn B | Ngưỡng và định nghĩa "một người xác nhận" đã công bố trước khi phát form. Sửa định nghĩa lúc này là gian lận phương pháp. Dữ liệu vẫn cho hai tín hiệu hẹp hơn (11/20 ở C2, 18/20 ở C3) nhưng không đủ để thoả điều kiện kép |
| 17/9 · CP3 | Chốt **một** bộ eval chính thức: 25 case Python (84%). Bộ Node 20 case (95%) lùi thành lịch sử CP2 | Hai bộ cho hai con số khác nhau trong cùng `spec.md` (§4 ghi 84%, §7 ghi 95%). Bộ Python có taxonomy đủ 4 lớp chỗ khó, có log thô từng lời gọi LLM, và là bộ duy nhất `index.html` hiện tại chạy được |
| 17/9 · CP3 | Đưa nguồn đối chiếu ra thư mục `codebase/knowledge/` (5 pack: hallucination, toolcall, grounding, eval-first, automation-level), chọn bằng `MINILAB_TOPIC`; bản mẫu nạp pack đang chạy qua `GET /api/scope` | Nguồn đối chiếu trước đó bị chép cứng ở hai chỗ (`agent/sources.py` và mảng `SRC` trong `index.html`) và đã một lần lệch nhau. Giờ chỉ còn một nguồn, và đổi khái niệm không phải sửa code |
| 17/9 · CP3 | Bỏ cổng chặn cứng "bài <40 ký tự → THIẾU_CĂN_CỨ" trong `core.py`; thay bằng cổng lĩnh vực trong prompt + `_guard()` kiểm sau | Bài lạc đề ngắn ("mỳ cay") bị cổng độ dài chặn trước khi LLM kịp nhìn, nên luôn ra THIẾU_CĂN_CỨ thay vì NGOÀI_PHẠM_VI. Đếm ký tự không phân biệt được "chưa đủ nội dung" với "nói chuyện khác" |
| 17/9 · CP3 | Bắt LLM trích `matched_evidence` (nguyên văn chữ học viên) cho từng tiêu chí, Python dò lại trong bài trước khi cho `ĐỦ_CĂN_CỨ` | Lớp lỗi G14: LLM khai khớp đủ 3 tiêu chí trong khi bài chỉ nói 1 ý. Đây là lỗi đắt nhất theo chính §4 (false-positive), nên phải chặn deterministic chứ không tin lời LLM |
| 17/9 · CP3 | Chạy lại golden set sau các thay đổi trên: **84% → 96% (24/25)**; thêm bộ đo thứ hai `run_kb_check` 45 ca (100%) | Code đã đổi thì số cũ không còn mô tả đúng hệ thống. Ngưỡng đạt §7 vẫn khoá nguyên ở ≥80%, chỉ giá trị đo được cập nhật |
| 17/9 · CP4 | **Khoá quality bar §7**: 4 điều kiện, 4 ngưỡng, chốt lúc 21:00. Ghi rõ đạt 3/4 và chưa đo 1 | Mốc CP4 chấm đúng việc "chốt thế nào là đạt **trước khi** biết kết quả". Đặt chuẩn sau khi đã thấy số thì con số không nói lên điều gì |
| 17/9 · CP4 | Khôi phục §7 và sửa §4 sau khi merge nhánh `tu` (`2895411`) ghi đè hai mục này về bản CP2 | Nhánh `tu` tách ra trước khi `fc92298` hạ cánh, nên bản cũ thắng lúc merge. Hậu quả: §4 khai quyết định trung tâm là *mock — heuristic đếm từ khoá* trong khi code đã gọi LLM thật từ CP3, và §7 mất toàn bộ bảng quality bar — đúng thứ CP4 chấm |
| 17/9 · CP4 | Dựng mới **§3 · Dữ liệu & nguồn sự thật** | Spec nhảy thẳng §2 → §4 từ CP1. Sản phẩm là một cỗ máy đối chiếu mà spec không có mục nào khai nguồn đối chiếu lấy từ đâu, cái gì được commit, cái gì không |
| 17/9 · CP4 | §5 từ 4 kịch bản lên **10 kịch bản**, mỗi kịch bản gắn một mã ca có thật và hành vi **thực đo** | 4 kịch bản cũ là mô tả kỳ vọng, không kiểm lại được. 10 kịch bản mới đều truy được về `golden_set.json` / `kb_cases.json` và về một lượt chạy có ghi log |
| 17/9 · CP4 | Khai thẳng trong §3 và §7 rằng repo đang có **hai stack** với **hai bộ mã đoạn khác nhau**, chỉ trùng đúng `T06-138` | Bộ A chạy bản mẫu nhưng nguồn còn MOCK; bộ B có transcript thật nhưng không chạy được bản mẫu. Chọn một bên rồi im lặng thì người chấm mở repo ra vẫn thấy bên kia |
| 17/9 · CP4 | Thêm **§10 · Tự khai phần chưa làm xong** — 8 mục, kể cả mục bất lợi | Luật CP4: *khai thiếu không bị trừ điểm, giấu mới bị* |

---

## §10. Tự khai — phần chưa làm xong

*Bắt buộc của mốc CP4. Liệt kê đầy đủ tại thời điểm chốt spec, 17/9/2026 — kể cả những mục bất lợi cho điểm của nhóm.*

### Chưa làm — ảnh hưởng trực tiếp đến điểm

| # | Chưa xong cái gì | Hệ quả | Ai · bao giờ |
|---|---|---|---|
| 1 | **`validation/` chưa tồn tại** — 0 người ngoài nhóm đã dùng thử, 0 phiên, 0 quote | Khối **R6 = 8 điểm** chưa có gì chấm. Không làm thì trần điểm của nhóm là **92** | Cả nhóm · trước 13:00 18/9 |
| 2 | **Bảng willing users trống hoàn toàn** — `spec.md` §8 và `teammates.md` đều 0 tên | R6 yêu cầu 5 người thử, trong đó **2 người phải đã khai từ CP1**. Khai muộn có rủi ro không được tính | Đội trưởng · tối 17/9 |
| 3 | **Điều kiện 4 của quality bar chưa đo** — chỉ số HỌC của track D | Quality bar §7 dừng ở **đạt 3/4**. Đây là điều kiện duy nhất trả lời được câu "sản phẩm có làm người ta học được không" | Phụ thuộc mục 1 |
| 4 | **`reflection/` chưa tồn tại** — 0/4 file | Reflection cá nhân chấm riêng theo rubric của khoá | Mỗi người tự viết · trước CP5 |
| 5 | **`demo-slides.pdf` và video demo dự phòng chưa có** | Hai deliverable của CP5 | 18/9 |

### Nợ kỹ thuật — đã biết, chưa trả

| # | Nợ gì | Đã khai ở đâu |
|---|---|---|
| 6 | **Nguồn đối chiếu của stack chính vẫn là fixture MOCK.** Bốn mã `T06-138/141/145/149` trong `codebase/knowledge/hallucination.json` **chưa từng được đối chiếu với `transcript-06-clean.md` thật** — chúng được đặt ra ở CP2 khi data pack không còn trên máy. Stack Node đã xác minh một bộ mã khác (`T06-136/138/139/148`); hai bộ chỉ trùng `T06-138` | §3, §7 |
| 7 | **Hai stack song song chưa gộp.** Python chạy bản mẫu nhưng nguồn MOCK; Node có transcript thật nhưng không phục vụ được bản mẫu. Số chính thức lấy theo stack chạy bản mẫu | §7 |
| 8 | **Ca `G02` (attention) vẫn trượt** — lớp ① nguồn sự thật. Cần few-shot example trong prompt; mô tả bằng lời chưa đủ để phân biệt "khái niệm có thật nhưng ngoài bốn đoạn" với "nói sai trong phạm vi" | §5 dòng 2, §7 |

### Đã khai từ trước, nhắc lại để không bị hiểu là giấu

- **Khảo sát chuẩn A không đạt ngưỡng đã khoá: 2/20 = 10%, cần > 50%.** Nhóm giữ nguyên định nghĩa `a ∧ b` đã công bố trước khi phát form, không sửa định nghĩa sau khi xem dữ liệu, và đã thu hẹp phát biểu ở §1 cho khớp. Lát cắt D3 hiện đứng trên bằng chứng hành vi chuẩn B (99,81% · 0,03%), không đứng trên khảo sát.
- **Một lượt chạy đi sai (64%) được giữ nguyên trong báo cáo** thay vì xoá — §7.

### Không phải "chưa làm", mà là cố ý không làm

Bốn non-goals ở §4 (không chấm điểm · một bài một khái niệm · persona cố định · một agent) là **quyết định thu hẹp phạm vi**, không phải việc còn nợ. Lý do và cái giá của từng quyết định đã ghi ở §4.

