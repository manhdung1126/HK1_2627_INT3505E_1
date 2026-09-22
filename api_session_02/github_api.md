5 endpoint của GitHub REST API
Base URL: https://api.github.com

1. /users/{username}
Endpoint này trả thông tin của một user

Method: GET
Status code: 200 OK, 404 Not Found
Headers: Accept, X-GitHub-Api-Version

Có RESTful vì URI sử dụng danh từ users để biểu diễn resource và username để xác định một resource cụ thể. HTTP method GET được dùng đúng mục đích đọc dữ liệu

2. /repos/{owner}/{repo}
Endpoint này trả thông tin của một repository cụ thể

Method: GET
Status code: 200 OK, 301 Moved Permanently, 403 Forbidden, 404 Not Found
Headers: Accept, Authorization, X-GitHub-Api-Version

Có RESTful vì URI sử dụng danh từ repos để biểu diễn resource repository, còn owner và repo giúp xác định repository cụ thể. HTTP method GET được sử dụng đúng mục đích để lấy dữ liệu mà không thay đổi resource

3. /repos/{owner}/{repo}/issues
Endpoint này trả danh sách các issue của một repository

Method: GET
Status code: 200 OK, 301 Moved Permanently, 404 Not Found, 422 Unprocessable Content
Headers: Accept, Authorization, X-GitHub-Api-Version, Link

Có RESTful vì URI sử dụng các danh từ repos và issues để biểu diễn quan hệ giữa repository và collection các issue. HTTP method GET được dùng để đọc danh sách resource. Header Link có thể được sử dụng để hỗ trợ phân trang khi kết quả có nhiều trang

4. /repos/{owner}/{repo}/issues
Endpoint này tạo một issue mới trong repository

Method: POST
Status code: 201 Created, 400 Bad Request, 403 Forbidden, 404 Not Found, 410 Gone, 422 Unprocessable Content, 503 Service Unavailable
Headers: Accept, Authorization, X-GitHub-Api-Version

Có RESTful vì client gửi POST tới collection resource /issues để tạo một resource mới. URI vẫn sử dụng danh từ thay vì các động từ như /createIssue, và status code 201 Created thể hiện đúng ý nghĩa của việc tạo resource thành công

5. /repos/{owner}/{repo}/issues/{issue_number}
Endpoint này cập nhật thông tin của một issue cụ thể

Method: PATCH
Status code: 200 OK, 301 Moved Permanently, 403 Forbidden, 404 Not Found, 410 Gone, 422 Unprocessable Content, 503 Service Unavailable
Headers: Accept, Authorization, X-GitHub-Api-Version

Có RESTful vì URI xác định rõ một resource issue thông qua issue_number. HTTP method PATCH được sử dụng đúng mục đích để cập nhật một phần thông tin của resource thay vì thay thế toàn bộ resource