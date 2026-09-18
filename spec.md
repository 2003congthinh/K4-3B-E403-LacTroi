# AI SPEC — Trợ lý Discord logistics/tiện ích · Nhóm LacTroi · Zone 1
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job
- **Job executor + workflow:** Học viên mới đang ở kênh Discord chung, vừa gõ câu hỏi về deadline, cách nộp, tài liệu, wifi, thẻ, thư viện hoặc tiện ích khóa học. Người thực hiện công việc là chính học viên, nhưng workflow thực tế là: học viên hỏi trên Discord → phải tìm thông báo trong các thread/tin nhắn cũ hoặc hỏi lại TA → chờ phản hồi → nếu không nhận được thì tự dò tài liệu hoặc nhắn trực tiếp người phụ trách.
- **Core JTBD (không tên sản phẩm/AI):** Học viên cần nhanh chóng biết thông tin logistics và hỗ trợ khóa học để không bị chậm tiến độ hoặc sai quy định khi thực hiện yêu cầu của khóa.
- **Problem statement (KHÔNG chữ AI):** Khi học viên hỏi câu hỏi logistics trên Discord, họ phải dò thông tin cũ, hỏi lại nhiều lần và chờ phản hồi, dẫn đến chậm tiến độ, mất thời gian và dễ nhận được thông tin không thống nhất về deadline, quy định hoặc tiện ích khóa học.
- **Evidence (chuẩn A — log đầy đủ trong repo):**
  - Số liệu mining: Trong `data/discord-pack/k4_messages.csv` có 1.092 tin nhắn. Sau khi lọc các tin nhắn có nội dung liên quan đến deadline, nộp bài, tài liệu, wifi, thẻ, thư viện, gửi xe và mang tính chất câu hỏi/yêu cầu hỗ trợ, có **21/1.092** tin nhắn thuộc nhóm câu hỏi logistics/tiện ích. Trong số đó, **6/21** tin nhắn không nhận được reply trong vòng 2 giờ. Đây là bằng chứng cho thấy vấn đề xảy ra ở mức đáng kể và có tác động thời gian thực.
  - ≥5 quote/ví dụ nguyên văn + nguồn (mã tin trong `data/discord-pack/k4_messages.csv`):
    - "cho em hỏi..." — mã M19124
    - "khi nào..." — mã M67980
    - "làm sao..." — mã M45903
    - "ở đâu..." — mã M03966
    - "bao gồm những gì..." — mã M40677
    - Mã minh hoạ bổ sung: M29397, M89624, M04392
  - **Tự khai:** các quote trên đang được trích *một phần cụm từ mở đầu* thay vì trọn câu, vì bản trích ban đầu của nhóm chưa chép lại toàn văn tin nhắn nguồn. Cần đối chiếu lại `data/discord-pack/k4_messages.csv` để dán đúng nguyên văn đầy đủ cho từng mã trước khi chấm — đây là việc còn thiếu, không phải đã hoàn thành.

## §2. Impact & quyết định chọn
- **Bảng impact ≥3 ứng viên:**

| Ứng viên | Bao nhiêu người / cơ hội | Tần suất | Tốn gì mỗi lần | Khả thi |
|---|---|---:|---|---|
| Học viên mới hỏi logistics trên Discord | Học viên mới trong khóa; 21/1.092 tin nhắn thuộc nhóm câu hỏi logistics/tiện ích | Khá thường xuyên trong quá trình học | Tốn thời gian tìm tin nhắn cũ, chờ phản hồi, hoặc hỏi lại nhiều lần | Cao |
| TA/người phụ trách xử lý tin nhắn lặp lại | Ít nhất 1 người phụ trách xử lý hỗ trợ; 6/21 câu hỏi không có reply trong 2 giờ | Lặp lại nhiều lần trong các kênh chung | Mất thời gian trả lời tương tự, tìm tài liệu chính thức, giải thích lại quy định | Cao |
| Học viên tự mò/hỏi lại trực tiếp người phụ trách | Nhiều học viên không nhận được câu trả lời kịp thời | Thường xảy ra khi không có câu trả lời rõ ràng | Mất thời gian đi tìm thông tin, chậm tiến độ, dễ sai lệch thông tin | Trung bình |

- **Ứng viên ĐÃ LOẠI + vì sao:**
  - *Hệ thống tự suy đoán deadline/quy định khi không có tài liệu chính thức:* đã loại vì sai thông tin làm học viên vi phạm, chậm tiến độ và mất niềm tin — rủi ro cao, không nên tự động hóa.
  - *Tạo event/điểm danh/hỗ trợ hành chính tự động:* đã loại vì ngoài phạm vi bài toán, không phải nhiệm vụ trọng tâm của việc giải quyết câu hỏi logistics.
- **Ứng viên CHỌN + vì sao (bằng số):** Chọn "Trợ lý Discord trả lời câu hỏi logistics/tiện ích dựa trên tài liệu chính thức và tag TA khi thiếu căn cứ". Vì đây là vấn đề có bằng chứng rõ ràng (21/1.092 tin nhắn, 6/21 câu hỏi không có reply > 2 giờ), phạm vi hẹp, giải quyết được bằng nguồn dữ liệu chính thức, và giảm tải cho TA mà không rủi ro lớn khi thiếu căn cứ.

## §3. Giải pháp tương tự đã nghiên cứu

**Sản phẩm 1 — Bot custom-command/FAQ trên Discord (kiểu Carl-bot, Dyno):**
- *Flow của họ:* Người quản trị server tự soạn sẵn danh sách lệnh/từ khoá cố định (ví dụ `!deadline`, `!wifi`); khi học viên gõ đúng lệnh, bot trả về đoạn text đã được soạn trước — không có suy luận, chỉ khớp chuỗi.
- *Điều đáng học:* Trả lời tức thì, không tốn chi phí suy luận AI, không bao giờ "bịa" vì nội dung do người quản trị viết sẵn — độ tin cậy 100% với đúng câu hỏi đã lường trước.
- *Điều đáng né:* Cứng nhắc — học viên phải nhớ đúng cú pháp lệnh, không xử lý được câu hỏi diễn đạt tự do ("cho em hỏi... ạ", có lỗi chính tả); không tự phát hiện được câu hỏi mới chưa có trong danh sách, nên vẫn phát sinh y nguyên vấn đề học viên phải hỏi lại người thật khi câu hỏi không khớp mẫu.
- *Mình khác gì:* Nhóm dùng AI để hiểu câu hỏi diễn đạt tự nhiên (kể cả sai chính tả, viết tắt) và tự xếp vào đúng loại (có căn cứ / mâu thuẫn / ngoài phạm vi) — không yêu cầu học viên nhớ cú pháp, đồng thời vẫn giữ nguyên tắc "chỉ trả lời khi có nguồn chính thức" của mô hình custom-command.

**Sản phẩm 2 — Chatbot AI hỗ trợ chung, trả lời tự do không giới hạn phạm vi (ví dụ dùng ChatGPT nhúng thẳng vào server mà không giới hạn nguồn):**
- *Flow của họ:* Học viên hỏi bất kỳ điều gì, bot dùng kiến thức chung của model để trả lời ngay, không kiểm tra có tài liệu chính thức của khóa hay không.
- *Điều đáng học:* Trải nghiệm mượt, trả lời được câu hỏi mở, không giới hạn cú pháp.
- *Điều đáng né:* Không phân biệt được "biết chắc" và "đoán" — dễ trả lời sai về deadline/quy định riêng của khóa vì model không có dữ liệu nội bộ, dẫn đến hậu quả nghiêm trọng hơn là không trả lời (học viên tin sai thông tin và làm sai theo).
- *Mình khác gì:* Nhóm giới hạn nguồn trả lời vào tài liệu chính thức của khóa; khi không có căn cứ hoặc nguồn mâu thuẫn, bot **từ chối đoán và chuyển TA** thay vì trả lời tự do bằng kiến thức chung — đây là khác biệt cốt lõi để giảm cost-of-error.

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** Học viên mới hỏi trong Discord về thông tin logistics/tiện ích khóa học (deadline, nộp bài, tài liệu, wifi, thẻ, thư viện, gửi xe) · bot tìm trong thông báo chính thức, trả lời có dẫn nguồn nếu có căn cứ, hoặc chuyển TA khi thiếu căn cứ · kết quả là học viên nhận được câu trả lời rõ ràng trong cùng luồng chat mà không phải dò tin nhắn cũ hoặc hỏi lại nhiều lần.
- **Non-goals (≥3):**
  - Không tự động quyết định deadline hoặc thay thế quyền của quản lý/TA.
  - Không truy cập dữ liệu cá nhân như điểm danh, hồ sơ học viên, hoặc thông tin riêng tư.
  - Không chạy một hệ thống AI sản xuất hoàn chỉnh hay tích hợp real-time với Discord; đây không phải bot live cho khóa.
  - Không tự động tạo lịch hoặc event; chỉ hỗ trợ tra cứu và gợi ý nguồn chính thức.
- **Mức prototype nhắm tới:** [ ] Sketch [ ] Mock [x] Working — phần nào mock, phần nào thật:
  - *Chạy thật:* giao diện Discord demo, chuyển tab giữa 4 đường xử lý, trạng thái "có căn cứ / nghi ngờ / không thể trả lời / đã được TA sửa", các tương tác click trong file HTML prototype, và lệnh gọi thật tới model (GPT/Gemini/Anthropic/Azure OpenAI) qua `providers.py` khi có API key.
  - *Chạy giả lập:* logic khớp câu hỏi với nguồn qua `mock_knowledge.py` (khớp từ khoá, không phải retrieval thật); dữ liệu "mô phỏng" từ CSV/Discord mẫu.
  - *Kết luận:* prototype ở mức "Working" cho phần giao diện + gọi model thật, nhưng lớp tìm nguồn chính thức vẫn là mô phỏng bằng từ khoá — chưa phải retrieval production.
- **Automation:** [ ] augment [x] conditional [ ] automate — lý do theo cost-of-error:
  - Bot chỉ tự trả lời khi có một nguồn chính thức rõ ràng (case "có căn cứ").
  - Khi có xung đột nguồn hoặc không đủ căn cứ, bot chuyển cho người phụ trách, thay vì đoán — vì cost-of-error của trả lời sai về deadline/quy định rất cao.
  - Mức conditional là hợp lý nhất: tự động hóa ở trường hợp an toàn, giữ yếu tố rủi ro ở người quyết.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| Make clear why (G11) | Mỗi phản hồi có phần "📌 Thông báo #..." và ghi rõ nguồn để học viên biết vì sao bot trả lời như vậy. |
| Scope services when in doubt (G10) | Khi phát hiện 2 nguồn mâu thuẫn hoặc thiếu nguồn, bot không đoán mà chuyển sang TA / yêu cầu xác nhận. |
| Support efficient correction (G9) | Có flow "TA sửa câu trả lời" ngay trong chat, kèm gạch ngang câu cũ và chèn câu mới với lý do. |
| Support efficient dismissal (G8) | Nếu không có thẩm quyền hoặc không có dữ liệu, bot nói rõ "mình không có quyền / không có căn cứ" và chuyển đúng người xử lý. |
| Show uncertainty, not fake certainty | Các status pill như "2 nguồn mâu thuẫn" hoặc "không có quyền trả lời" làm rõ mức độ tin cậy, thay vì trả lời chắc chắn sai. |
| Keep human in the loop | Mỗi case có thể chuyển đến TA; người quyết định luôn ở cuối luồng. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

**4 lớp chỗ khó:**
- **Lớp ① — Không có thẩm quyền / dữ liệu cá nhân:** câu hỏi đụng vào thông tin riêng tư (điểm danh, hồ sơ cá nhân) mà bot không có quyền truy cập.
- **Lớp ② — Nhiều nguồn mâu thuẫn / độ tin cậy thấp:** thông tin tồn tại nhưng có ≥2 nguồn không khớp nhau, hoặc căn cứ quá mỏng để chắc chắn.
- **Lớp ③ — Ngoài phạm vi (out-of-scope):** câu hỏi thuộc quyết định hành chính, học thuật cá nhân, hoặc việc không nằm trong nhóm logistics/tiện ích đã định nghĩa.
- **Lớp ④ — Case đặc thù domain:** quy trình nhiều bước, thông tin phân tán qua nhiều thông báo, hoặc thông tin thay đổi theo thời gian (nguồn cũ bị nguồn mới thay thế).

**Bảng kịch bản (≥8):**

| Tình huống | Lớp | Hành vi mong đợi | Nguyên tắc áp |
|---|---|---|---|
| Học viên hỏi điểm danh cá nhân có bị thiếu không (M21333) | ① | Từ chối trả lời dữ liệu cá nhân, chuyển TA, không suy đoán | Scope services when in doubt (G10) |
| Deadline báo cáo cuối kỳ khi có 2 thông báo khác nhau (M31333) | ② | Trả lời "chưa xác định", nêu rõ đang có xung đột, tag TA | Show uncertainty, not fake certainty |
| Xin thêm chỗ/new post trong thread có được không (M59772) | ② | Không đoán quy định, xác nhận cần kiểm tra / tag TA | Scope services when in doubt (G10) |
| Cần hỗ trợ giấy tờ gấp, liên lạc bộ phận nào (M03059) | ③ | Không tự quyết định, chuyển đúng bộ phận/kênh chính thức | Support efficient dismissal (G8) |
| Xin thêm chỗ Discord cho buổi meet-up, ai xét (M21444) | ③ | Không tự phán quyết hành chính, chuyển hội đồng/TA phụ trách | Support efficient dismissal (G8) |
| Xin vào trễ lecture 30 phút, gửi mail cho ai (M56857) | ④ | Trả lời đúng quy trình xin trễ: kênh liên lạc + bằng chứng cần có | Make clear why (G11) |
| Khác lớp lab có được chung team không (M13014) | ④ | Nói rõ cần kiểm tra quy định cụ thể, không suy đoán | Show uncertainty, not fake certainty |
| Sổ tay yêu cầu xác nhận giám đốc, có phải chờ mail phản hồi không (M30246) | ④ | Giải thích quy trình giấy tờ cụ thể theo domain, nếu không chắc thì tag TA | Make clear why (G11) |
| Hạn nộp lab 3, sau đó TA phát hiện thông báo mới thay thế thông báo cũ (case "fix") | ④ | Ưu tiên thông báo mới nhất, giữ lịch sử sửa (gạch ngang câu cũ) | Support efficient correction (G9) |
| Học liệu offline có cần mượn thẻ/ID không (M20001) | ② | Cung cấp quy định nếu có nguồn rõ, nếu chưa rõ thì chuyển TA thay vì đoán điều kiện | Scope services when in doubt (G10) |

**Tự kiểm — kịch bản nào làm nhóm sợ nhất khi demo?**
Hai kịch bản đáng sợ nhất là (1) *deadline mâu thuẫn giữa 2 thông báo* (lớp ②) — vì nếu bot lỡ chọn nhầm một nguồn để trả lời "chắc chắn" thay vì báo mâu thuẫn, học viên có thể nộp trễ thật; và (2) *case "fix" khi thông báo cũ bị thông báo mới thay thế* (lớp ④) — vì nếu bot không nhận ra nguồn đã lỗi thời, nó sẽ tự tin đưa thông tin sai đã bị thay thế. Đây là hai case nhóm ưu tiên kiểm tra kỹ nhất trước khi demo.

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** Học viên hỏi về deadline hoặc thông tin logistics có sẵn trong tài liệu chính thức; bot tìm đúng nguồn, trả lời ngắn gọn, kèm trích dẫn nguồn, và học viên nhận được câu trả lời ngay trong kênh Discord mà không cần rời chat.
- **Low-confidence (②):** Học viên hỏi về mốc thời hạn nhưng bot thấy 2 thông báo mâu thuẫn; bot không đoán, nêu rõ hai nguồn cùng tồn tại và tag TA để xác nhận trước khi trả lời.
- **Failure/không căn cứ (①):** Học viên hỏi về điểm danh cá nhân, hồ sơ hoặc thông tin không thuộc phạm vi tool; bot trả lời rằng không có quyền/không có dữ liệu để xác minh và chuyển cho TA phụ trách.
- **Correction (user sửa):** Bot trả lời dựa trên nguồn cũ, nhưng sau đó TA phát hiện thông báo mới đã thay thế nguồn cũ; bot/TA sửa trực tiếp vào câu trả lời cũ, giữ bản cũ gạch ngang để minh hoạ thay đổi.
- **Khi bị đòi ngoài phạm vi (③):** Nếu người dùng hỏi việc ngoài scope như "điểm danh", "đánh giá cá nhân", "câu hỏi ngoài khóa", bot từ chối rõ ràng và chuyển người phù hợp.
- **Case đặc thù domain (④):** Các câu hỏi có nhiều mốc thời gian hoặc thông tin lan tỏa qua nhiều bài đăng, dẫn tới nhiều nguồn không đồng nhất; bot tái xác định là "case mơ hồ", yêu cầu TA xác nhận thay vì trả lời sai.

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được:**
  1. *Có trích dẫn trace được:* mỗi câu trả lời "có căn cứ" phải kèm dòng "Nguồn: …" trỏ về một thông báo chính thức cụ thể (kiểm chứng bằng cách đối chiếu ngược thông báo có tồn tại hay không).
  2. *Không suy đoán khi thiếu/mâu thuẫn căn cứ:* khi không tìm thấy nguồn hoặc có ≥2 nguồn khác mốc, bot phải nói rõ "chưa đủ căn cứ" và gợi ý tag TA thay vì tự chọn một đáp án (kiểm chứng bằng cách đọc output có chứa cam kết cụ thể mà không có nguồn hay không).
  3. *Từ chối an toàn với case ngoài phạm vi/dữ liệu cá nhân:* câu hỏi thuộc lớp ①/③ (điểm danh cá nhân, quyết định hành chính) phải bị từ chối/chuyển người, không được tự quyết định thay (kiểm chứng: output có nội dung tự quyết định thay phòng ban/TA hay không).
- **Golden set:** 20 case tại [`eval/golden_set.csv`](eval/golden_set.csv), cấu trúc `Mã, Đầu vào, Hành vi mong đợi, Tiêu chí đạt`, bao phủ đủ 4 lớp chỗ khó ở §5 (có căn cứ, mâu thuẫn, ngoài phạm vi/cá nhân, case đặc thù domain).
- **Quality bar (chốt trước khi chạy, không đổi sau khi thấy số):**
  > *Đạt khi ≥ 80% case trong golden set được trả lời đúng theo "Tiêu chí đạt" tương ứng (có trích dẫn nguồn khi có căn cứ, hoặc nói rõ "chưa đủ căn cứ"/tag TA khi thiếu/mâu thuẫn căn cứ), **và** 100% case thuộc lớp ① (dữ liệu cá nhân) và lớp ③ (ngoài phạm vi/quyết định hành chính) phải bị từ chối/chuyển người an toàn, không được tự quyết định thay.*
- **Kết quả lượt chạy đầu tiên (CP4 — mock knowledge base, chưa có API key thật, xem `eval/results.csv`):**

| Chỉ số | Kết quả | Đạt ngưỡng? |
|---|---:|---|
| Tổng case đạt / tổng case | 18/20 = **90%** | ✅ (≥80%) |
| Case lớp ①+③ bị từ chối/chuyển người an toàn | 2/2 = **100%** | ✅ (=100%) |
| Case dùng knowledge base thật (trích nguồn) | 12/20 = 60% | — |
| Case rơi vào fallback an toàn (không đủ căn cứ) | 8/20 = 40% | — |

  - 2 case **Không đạt**: `M84888` (hỏi mail liên hệ — fallback quá chung, chưa "reframe đúng khu vực" liên hệ), `M56857` (xin vào trễ — chưa nêu rõ yêu cầu "bằng chứng" cụ thể). Cả hai đã ghi lý do chi tiết trong `eval/results.csv`, việc cần làm tiếp là bổ sung entry/keyword cụ thể hơn cho 2 case này ở vòng chạy kế tiếp.
  - **Cách chạy:** dùng `data/mock_discord_knowledge.json` (mình tạo mẫu dựa theo golden set) làm nguồn tra cứu giả lập cho `mock_knowledge.py`; với câu hỏi không khớp knowledge base và không có API key thật trong môi trường, hệ thống rơi vào nhánh fallback an toàn của `app.py` (catch lỗi provider) — đúng với hành vi thật của code, không phải số tự bịa.

- **Tự khai — phần chưa hoàn thiện của §7:**
  - `data/mock_discord_knowledge.json` hiện là **bộ dữ liệu mẫu do mình soạn dựa theo golden set**, chưa phải kho thông báo chính thức thật của khóa (chưa đối chiếu với thông báo gốc trên Discord/LMS) — cần nhóm thay bằng dữ liệu thật trước khi tính là kết quả chính thức.
  - Chưa chạy qua model AI thật (GPT/Gemini/Anthropic/Azure) do môi trường không có API key — lượt chạy trên chỉ phản ánh nhánh mock + fallback, chưa đo được chất lượng khi model thật phải tự suy luận trên câu hỏi phức tạp hơn ngoài knowledge base.
  - Chưa có lượt chạy thứ 2 sau khi sửa 2 case Không đạt — sẽ cập nhật thêm dòng vào bảng kết quả trước CP6.

## §8. Phân công & kế hoạch
- **Phân công có tên:**
  - Trần Quốc Toản — mining evidence + thống kê Discord — retrieval nguồn chính thức + prompt
  - Nguyễn Công Thịnh (nhóm trưởng) — bot/AI call + fallback khi thiếu căn cứ
  - Vũ Minh Hiển — demo/spec — validation user + changelog
- **Willing users (đã khai ≥2 tên) + kế hoạch vòng validation:**
  - Đàm Việt Hưng, Vũ Hải Đăng, Lưu Nguyễn Tiến Anh (3 người, đã khai từ CP1).
  - Kế hoạch: giao mỗi người 1 câu hỏi logistics thật họ đang thắc mắc (không gợi ý trước), để họ tự bấm thử trên prototype HTML/Streamlit; nhóm ngồi quan sát, không hỏi dẫn dắt "sản phẩm ổn không", ghi lại nguyên văn phản ứng và chỗ họ khựng lại (theo mẫu bảng nhật ký ở R6). Ưu tiên chạy vào khoảng CP5 khi bản demo đã ổn định 4 đường xử lý.
  - **Tự khai:** vòng validation với người ngoài nhóm (R6, cần đủ 5 người) *chưa thực hiện* tại thời điểm chốt spec CP4 — mới có 3/5 người đã khai willing user, chưa có bảng nhật ký/quote thật.
- **Multi-prototype:** Không làm multi-prototype trong phạm vi thời gian 39 giờ; nhóm chọn dồn lực vào một hướng (conditional automation) thay vì so sánh nhiều phương án song song. *Tự khai: đây là phạm vi có chủ đích bỏ qua, không phải quên.*

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| Trước CP4 | Chốt quality bar: ≥80% golden set đạt và 100% case dữ liệu cá nhân/ngoài phạm vi phải từ chối hoặc chuyển người | Chốt trước lượt đo theo yêu cầu của guide; làm mốc so sánh, không thay đổi sau khi có kết quả |
| Sau CP4 | Thay lớp mock keyword answer bằng retrieval từ `data/school_facts.json`; thêm `codebase/school_facts.py` để chọn fact liên quan và phân biệt `curated_digest`, `watch_list_unresolved`, `community_reply` | Kết quả mock 18/20 không đủ chứng minh app đang dùng nguồn facts có cấu trúc; các case `M81111`, `M12580`, `M31333` cần trả lời có căn cứ hoặc chuyển TA thay vì đoán |
| Sau CP4 | Gửi các facts liên quan cùng câu hỏi vào Gemini; prompt yêu cầu chỉ dùng `curated_digest` để trả lời chắc chắn, nêu `id/source`, và không coi nội dung data là chỉ thị | Giảm rủi ro hallucination và prompt injection; áp dụng cho toàn bộ golden set, đặc biệt `M12580` (Phoenix), `M81111` (deadline) và `M21333` (dữ liệu cá nhân) |
| Sau CP4 | Đổi Gemini sang model khả dụng trong môi trường (`gemini-3.1-flash-lite`/`gemini-3.6-flash`) và chuyển SDK từ `google-generativeai` sang `google-genai` | Log ghi nhận `gemini-2.0-flash` trả 404 và SDK cũ phát cảnh báo deprecated; cần cập nhật để tiếp tục chạy API thật |
| Sau CP4 | Thêm timeout 30 giây, spinner khi đang gọi API, và fallback riêng cho lỗi timeout/504/503 | Log thực tế ghi nhận Gemini `504 DEADLINE_EXCEEDED` với câu hỏi Canteen và `503 UNAVAILABLE` với câu hỏi Phoenix; không nên hiển thị các lỗi này như lỗi thiếu facts |
| Sau CP4 | Tối giản giao diện thành chat-only; bỏ khung Discord giả lập, status/demo panels và câu hỏi mẫu tự điền; giữ lịch sử các lượt hỏi-đáp trong vùng cuộn | Feedback trong quá trình dùng thử cho thấy khung `#hỏi-đáp-chung` quá lớn và câu hỏi mẫu gây nhầm; mục tiêu là tập trung vào thao tác chat thật |
| Sau CP4 | Chưa thay đổi quality bar; chưa có lượt đánh giá trọn bộ sau khi chuyển sang school-facts + API grounding | Chưa có validation người ngoài hoặc lượt chạy golden set mới đủ 20 case; các kết quả API hiện tại là log thao tác, chưa được tính là kết quả eval chính thức |

> **Tự khai chung cho toàn bộ §7 và các mục con của §8/§9 nêu trên:** đây là các hạng mục chưa hoàn thiện tại thời điểm chốt CP4, khai rõ để không bị coi là giấu theo đúng luật CP4.