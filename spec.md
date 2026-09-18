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
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

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
