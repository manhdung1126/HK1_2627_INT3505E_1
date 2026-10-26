# 5 lỗi có thể lộ

## 1. Lộ mật khẩu
- Mật khẩu lưu dạng rõ có thể bị đọc khi cơ sở dữ liệu bị lộ
- Cách tránh: băm mật khẩu, không trả mật khẩu hoặc mã băm trong response

## 2. Lộ token
- Token có thể bị lấy khi truyền qua HTTP, đặt trong URL hoặc ghi vào log
- Cách tránh: dùng HTTPS, gửi token qua header Authorization, không ghi token hoặc mật khẩu vào log

## 3. Đoán mật khẩu và dò email
- Thử đăng nhập nhiều lần để đoán mật khẩu. Thông báo lỗi riêng có thể làm lộ email đã đăng ký
- Cách tránh: giới hạn số lần đăng nhập. Trả cùng thông báo khi email hoặc mật khẩu sai

## 4. Chấp nhận token sai hoặc token cũ
- Token bị sửa, hết hạn hoặc đã bị thu hồi vẫn được dùng để truy cập API
- Cách tránh: kiểm tra chữ ký JWT, thuật toán cho phép, hạn dùng, nơi cấp, nơi nhận và loại token. Vô hiệu refresh token cũ sau khi cấp token mới. Thu hồi phiên nếu phát hiện dùng lại refresh token cũ

## 5. Lộ bài viết riêng tư
- Người dùng đổi ID trên URL để đọc bài private của người khác
- Cách tránh: kiểm tra scope posts:read và quyền trên bài viết. Bài private chỉ cho tác giả xem
