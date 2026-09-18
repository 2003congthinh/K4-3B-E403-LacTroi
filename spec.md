# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 18/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ): Học viên mới đang ở kênh Discord chung, vừa gõ câu hỏi về deadline, cách nộp, tài liệu, wifi, thẻ, thư viện hoặc tiện ích khóa học. Người thực hiện công việc là chính học viên, nhưng workflow thực tế là: học viên hỏi trên Discord → phải tìm thông báo trong các thread/tin nhắn cũ hoặc hỏi lại TA → chờ phản hồi → nếu không nhận được thì tự dò tài liệu hoặc nhắn trực tiếp người phụ trách.
- Core JTBD (không tên sản phẩm/AI trong câu): Học viên cần nhanh chóng biết thông tin logistics và hỗ trợ khóa học để không bị chậm tiến độ hoặc sai quy định khi thực hiện yêu cầu của khóa.
- Problem statement (KHÔNG chữ AI): Khi học viên hỏi câu hỏi logistics trên Discord, họ phải dò thông tin cũ, hỏi lại nhiều lần và chờ phản hồi, dẫn đến chậm tiến độ, mất thời gian và dễ nhận được thông tin không thống nhất về deadline, quy định hoặc tiện ích khóa học.
- Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - Số liệu mining / kết quả khảo sát (n = ?, % xác nhận): Trong `data/discord-pack/k4_messages.csv` có 1,092 tin nhắn. Sau khi lọc các tin nhắn có nội dung liên quan đến deadline, nộp bài, tài liệu, wifi, thẻ, thư viện, gửi xe và mang tính chất câu hỏi/yêu cầu hỗ trợ, có 21/1,092 tin nhắn thuộc nhóm câu hỏi logistics/tiện ích. Trong số đó, 6/21 tin nhắn không nhận được reply trong vòng 2 giờ. Đây là bằng chứng cho thấy vấn đề xảy ra ở mức đáng kể và có tác động thời gian thực.
  - ≥5 quote/ví dụ nguyên văn + nguồn:
    - "cho em hỏi..." — nguồn: `data/discord-pack/k4_messages.csv` (mã ví dụ: M19124)
    - "khi nào..." — nguồn: `data/discord-pack/k4_messages.csv` (mã ví dụ: M67980)
    - "làm sao..." — nguồn: `data/discord-pack/k4_messages.csv` (mã ví dụ: M45903)
    - "ở đâu..." — nguồn: `data/discord-pack/k4_messages.csv` (mã ví dụ: M03966)
    - "bao gồm những gì..." — nguồn: `data/discord-pack/k4_messages.csv` (mã ví dụ: M40677)
    - Bổ sung các mã minh họa khác: M29397, M89624, M04392, M40677, M45903, M67980, M19124.

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):

| Ứng viên | Bao nhiêu người / cơ hội | Tần suất | Tốn gì mỗi lần | Khả thi |
|---|---|---:|---|---|
| Học viên mới hỏi logistics trên Discord | Học viên mới trong khóa; 21/1,092 tin nhắn thuộc nhóm câu hỏi logistics/tiện ích | Khá thường xuyên trong quá trình học | Tốn thời gian tìm tin nhắn cũ, chờ phản hồi, hoặc hỏi lại nhiều lần | Cao |
| TA/Người phụ trách xử lý tin nhắn lặp lại | Ít nhất 1 người phụ trách xử lý hỗ trợ; 6/21 câu hỏi không có reply trong 2 giờ | Lặp lại nhiều lần trong các kênh chung | Mất thời gian trả lời tương tự, tìm tài liệu chính thức, và giải thích lại quy định | Cao |
| Học viên tự mò / hỏi lại trực tiếp | Nhiều học viên không nhận được câu trả lời kịp thời | Thường xảy ra khi không có câu trả lời rõ ràng | Mất thời gian đi tìm thông tin, chậm tiến độ, dễ sai lệch thông tin | Trung bình |

- Ứng viên ĐÃ LOẠI + vì sao:
  - Hệ thống tự suy đoán deadline / quy định khi không có tài liệu chính thức: đã loại vì sai thông tin về quy định hoặc deadline làm học viên vi phạm, chậm tiến độ và làm mất niềm tin. Đây là quyết định có rủi ro cao và không nên tự động hóa.
  - Tạo event / điểm danh / hỗ trợ hành chính tự động: đã loại vì ngoài phạm vi của bài toán, không phải là nhiệm vụ trọng tâm của việc giải quyết câu hỏi logistics.
- Ứng viên CHỌN + vì sao (bằng số): Chọn “Trợ lý Discord trả lời câu hỏi logistics/tiện ích dựa trên tài liệu chính thức và tag TA khi thiếu căn cứ”. Vì đó là vấn đề có bằng chứng rõ ràng (21/1,092 tin nhắn, 6/21 câu hỏi không có reply > 2 giờ), phạm vi hẹp và có thể giải quyết bằng nguồn dữ liệu chính thức, đồng thời giảm tải cho TA mà không rủi ro quá lớn khi thiếu căn cứ. 

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả): Học viên mới hỏi trong Discord về thông tin logistics/tiện ích khóa học (deadline, nộp bài, tài liệu, wifi, thẻ, thư viện, gửi xe) · bot tìm trong thông báo chính thức, trả lời có dẫn nguồn nếu có căn cứ, hoặc chuyển TA khi thiếu căn cứ · kết quả là học viên nhận được câu trả lời rõ ràng trong cùng luồng chat mà không phải dò tin nhắn cũ hoặc hỏi lại nhiều lần.
- Non-goals (≥3 thứ KHÔNG build):
  - Không tự động quyết định deadline hoặc thay thế quyền của quản lý/TA.
  - Không truy cập dữ liệu cá nhân như điểm danh, hồ sơ học viên, hoặc thông tin riêng tư.
  - Không chạy một hệ thống AI sản xuất hoàn chỉnh hay tích hợp real-time với Discord; đây không phải bot live cho khóa.
  - Không tự động tạo lịch hoặc event; chỉ hỗ trợ tra cứu và gợi ý nguồn chính thức.
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working — phần nào mock, phần nào thật:
  - Chạy thật: giao diện Discord demo, chuyển tab giữa 4 đường xử lý, trạng thái “có căn cứ / nghi ngờ / không thể trả lời / đã được TA sửa”, và các tương tác click trong file HTML prototype.
  - Chạy giả lập: loại câu hỏi, logic chọn nguồn, mức độ tự động hóa, phản hồi bot, và dữ liệu “mô phỏng” từ CSV/Discord mẫu; không có retrieval từ hệ thống thực tế và không có AI live inference.
  - Kết luận: đây là một prototype “Working” ở mức interactive demo, nhưng logic điều phối và phản hồi là mô phỏng để chứng minh trải nghiệm, không phải phiên bản production.
- Automation: [ ] augment [x] conditional [ ] automate — lý do theo cost-of-error:
  - Bot chỉ tự trả lời khi có một nguồn chính thức rõ ràng (case “có căn cứ”).
  - Khi có xung đột nguồn hoặc không đủ căn cứ, bot chuyển cho người phụ trách, thay vì đoán. Đây là lựa chọn phù hợp vì cost-of-error của trả lời sai về deadline/quy định rất cao.
  - Mức conditional là hợp lý nhất cho mô hình này: thực hiện tự động hóa ở những trường hợp an toàn, còn yếu tố rủi ro được giữ ở người quyết.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | Make clear why (G11) | Mỗi phản hồi có phần "📌 Thông báo #..." và ghi rõ nguồn để học viên biết vì sao bot trả lời như vậy. |
  | Scope services when in doubt (G10) | Khi phát hiện 2 nguồn mâu thuẫn hoặc thiếu nguồn, bot không đoán mà chuyển sang lãnh vực TA / yêu cầu xác nhận. |
  | Support efficient correction (G9) | Có flow “TA sửa câu trả lời” ngay trong chat, kèm gạch ngang câu cũ và chèn câu mới với lý do. |
  | Support efficient dismissal (G8) | Nếu không có thẩm quyền hoặc không có dữ liệu, bot nói rõ “mình không có quyền / không có căn cứ” và chuyển đúng người xử lý. |
  | Show uncertainty, not fake certainty | Trong mockup, các status pill như “2 nguồn mâu thuẫn” hoặc “không có quyền trả lời” làm rõ mức độ tin cậy, thay vì trả lời chắc chắn sai. |
  | Keep human in the loop | Mỗi case có thể chuyển đến TA; prototype cho thấy người quyết định luôn ở cuối luồng. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: Học viên hỏi về deadline hoặc thông tin logistics có sẵn trong tài liệu chính thức; bot tìm đúng nguồn, trả lời ngắn gọn, kèm trích dẫn nguồn, và học viên nhận được câu trả lời ngay trong kênh Discord mà không cần rời chat. Đây là trường hợp có căn cứ rõ ràng và mức tin cậy cao.
- Low-confidence (②): Học viên hỏi về mốc thời hạn nhưng bot thấy 2 thông báo mâu thuẫn; bot không đoán, nêu rõ hai nguồn cùng tồn tại và tag TA để xác nhận trước khi trả lời. Luồng này hiển thị rõ nguyên tắc tránh sai thông tin có hại.
- Failure/không căn cứ (①): Học viên hỏi về điểm danh cá nhân, hồ sơ hoặc thông tin không thuộc phạm vi tool; bot trả lời rằng không có quyền / không có dữ liệu để xác minh và chuyển cho TA phụ trách. Đây là case “không cho bot đoán”.
- Correction (user sửa): Bot trả lời dựa trên nguồn cũ, nhưng sau đó TA phát hiện thông báo mới đã thay thế nguồn cũ; bot/TA sửa trực tiếp vào câu trả lời cũ, giữ bản cũ gạch ngang để minh hoạ thay đổi. Đây là flow xử lý lỗi có thể sửa nhanh và không làm mất lịch sử.
- Khi bị đòi ngoài phạm vi (③): Nếu người dùng hỏi việc ngoài scope như “điểm danh”, “đánh giá cá nhân”, “câu hỏi ngoài khóa”, bot từ chối rõ ràng và chuyển người phù hợp. Đây là cách bảo vệ độ tin cậy và tránh chạm vào phạm vi nhạy cảm.
- Case đặc thù domain (④): Các câu hỏi có nhiều mốc thời gian hoặc thông tin lan tỏa qua nhiều bài đăng, dẫn tới nhiều nguồn không đồng nhất; bot tái xác định là “case mơ hồ”, yêu cầu TA xác nhận thay vì trả lời sai. Prototype dùng trạng thái “2 nguồn mâu thuẫn” để thể hiện điều đó.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```
