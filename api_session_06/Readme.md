## 1. POST /auth/login

### Scope
Không yêu cầu scope hoặc token. Người dùng đăng nhập bằng email và mật khẩu

### Lỗi có thể xảy ra
- JSON sai, thiếu email hoặc mật khẩu, hoặc dữ liệu không hợp lệ
- Email hoặc mật khẩu không đúng

### Status code
- `200 OK`: đăng nhập thành công, trả access token và refresh token
- `400 Bad Request`: dữ liệu gửi lên không hợp lệ
- `401 Unauthorized`: email hoặc mật khẩu không đúng

## 2. POST /auth/refresh

### Scope
Không yêu cầu scope. Cần refresh token hợp lệ trong header `Authorization: Bearer <refresh_token>`

### Lỗi có thể xảy r
- Không gửi refresh token
- Refresh token không hợp lệ, hết hạn hoặc đã bị thu hồi
- Gửi nhầm access token thay cho refresh token

### Status code
- `200 OK`: cấp access token và refresh token mới, vô hiệu refresh token cũ
- `401 Unauthorized`: thiếu refresh token, token không hợp lệ, hết hạn hoặc đã thu hồi

## 3. GET /posts/{id}

### Scope
Yêu cầu scope `posts:read` trong access token hợp lệ. Token được gửi trong header `Authorization: Bearer <access_token>`

### Lỗi có thể xảy ra
- ID không phải số nguyên dương.
- Thiếu access token, token không hợp lệ, hết hạn hoặc đã bị thu hồi.
- Gửi nhầm refresh token thay cho access token.
- Thiếu scope `posts:read`.
- Người dùng không phải tác giả của bài private.
- Không tìm thấy bài viết.

### Status code
- `200 OK`: trả thông tin bài viết
- `400 Bad Request`: ID không hợp lệ
- `401 Unauthorized`: thiếu access token, token không hợp lệ, hết hạn hoặc đã thu hồi
- `403 Forbidden`: thiếu scope `posts:read` hoặc không được xem bài private
- `404 Not Found`: không tìm thấy bài viết
