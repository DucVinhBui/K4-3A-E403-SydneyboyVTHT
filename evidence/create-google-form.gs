/**
 * Tạo Google Form khảo sát chuẩn A — Nhóm SydleyboyVTHT (K4-3A-E403)
 * Dùng: script.google.com > New project > dán file này > Run > cấp quyền > xem Execution log lấy link.
 * Nội dung câu hỏi khớp evidence/survey-questions.md
 */
function taoFormKhaoSat() {
  const form = FormApp.create('Khảo sát: cách mọi người học trong khoá AI20k');

  form.setDescription(
    'Khảo sát ngắn ~90 giây của một nhóm trong lớp 3A.\n\n' +
    'Không có câu trả lời đúng/sai. Mọi câu đều hỏi về LẦN GẦN NHẤT đã thật sự xảy ra với bạn — ' +
    'cứ trả lời đúng như nó đã diễn ra, kể cả khi bạn thấy nó không hay ho gì.\n\n' +
    'Cảm ơn bạn!'
  );

  form.setProgressBar(true)
      .setAllowResponseEdits(false)
      .setLimitOneResponsePerUser(false)
      .setShowLinkToRespondAgain(false)
      .setConfirmationMessage('Đã ghi nhận. Cảm ơn bạn nhiều!');

  // Bắt buộc ghi danh tính: chuẩn A yêu cầu log "ai trả lời"
  form.addTextItem()
      .setTitle('Họ tên + Mã học viên')
      .setHelpText('Ví dụ: Nguyễn Văn A — 2A202600000')
      .setRequired(true);

  // Câu 1 — bối cảnh hành vi
  form.addMultipleChoiceItem()
      .setTitle('1. Lần gần nhất học xong một khái niệm trong khoá (attention, RAG, agent, tokenization…), NGAY SAU ĐÓ bạn làm gì?')
      .setChoiceValues([
        'Đi thẳng sang phần tiếp theo',
        'Đọc lại slide một lượt nữa',
        'Hỏi AI tutor trên VLearn',
        'Tự làm bài tập/quiz về nó',
        'Giải thích lại cho bạn khác'
      ])
      .showOtherOption(true)
      .setRequired(true);

  // Câu 2 — ĐIỀU KIỆN XÁC NHẬN (a)
  form.addMultipleChoiceItem()
      .setTitle('2. Lần gần nhất bạn kết luận "mình hiểu rồi" về một khái niệm — bạn dựa vào đâu để kết luận như vậy?')
      .setHelpText('Chọn thứ bạn đã thật sự dựa vào lần đó, không phải thứ lẽ ra nên làm.')
      .setChoiceValues([
        'Thấy quen, đọc trôi được',
        'Đọc lại thấy ổn',
        'Tự làm được bài tập về nó',
        'Giải thích lại được cho người khác',
        'Có người kiểm tra lại và xác nhận'
      ])
      .showOtherOption(true)
      .setRequired(true);

  // Câu 3 — ĐIỀU KIỆN XÁC NHẬN (b)
  form.addMultipleChoiceItem()
      .setTitle('3. Đã bao giờ bạn phát hiện mình HIỂU SAI một khái niệm, sau khi đã tự cho là mình hiểu rồi chưa?')
      .setChoiceValues([
        'Có — tôi kể lại được lần đó',
        'Có — nhưng không nhớ rõ lần nào',
        'Chưa bao giờ'
      ])
      .setRequired(true);

  // Câu 4 — số liệu cho bảng impact
  form.addCheckboxItem()
      .setTitle('4. Lần đó bạn mất gì?')
      .setHelpText('Chọn nhiều được.')
      .setChoiceValues([
        'Mất điểm bài tập/quiz',
        'Mất thời gian làm lại',
        'Hiểu sai kéo sang các bài sau',
        'Ngại hỏi / mất tự tin',
        'Không mất gì đáng kể',
        'Chưa từng xảy ra'
      ])
      .setRequired(false);

  // Câu 5 — nguồn quote nguyên văn
  form.addParagraphTextItem()
      .setTitle('5. Kể ngắn lần đó: bạn đang học gì, hiểu sai chỗ nào, và phát hiện ra vào lúc nào?')
      .setHelpText('2–3 câu là đủ. Cứ viết tự nhiên.')
      .setRequired(true);

  // Câu 6 — câu phản chứng
  form.addParagraphTextItem()
      .setTitle('6. Có khi nào bạn thấy cách học hiện tại của mình là đủ, không cần ai kiểm tra lại không? Nếu có, kể một lần.')
      .setRequired(false);

  // Sheet nhận kết quả
  const ss = SpreadsheetApp.create('Ket qua khao sat chuan A — SydleyboyVTHT');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('================ LINK ================');
  Logger.log('Link gửi cho người trả lời : ' + form.getPublishedUrl());
  Logger.log('Link sửa form              : ' + form.getEditUrl());
  Logger.log('Google Sheet kết quả       : ' + ss.getUrl());
  Logger.log('=====================================');
}
