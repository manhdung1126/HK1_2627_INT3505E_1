# Lab 1:

## 1. Không gửi tài khoản và mật khẩu

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders
```

Response:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:31 GMT
Content-Type: application/json
Content-Length: 25
WWW-Authenticate: Basic realm="orders"
Connection: close

{"error":"unauthorized"}
```

## 2. Sai mật khẩu

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders -H 'Authorization: Basic YW5Adm51LmVkdS52bjp3cm9uZ3Bhc3N3b3Jk'
```

Response:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:31 GMT
Content-Type: application/json
Content-Length: 25
WWW-Authenticate: Basic realm="orders"
Connection: close

{"error":"unauthorized"}
```

## 3. Đăng nhập đúng

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders -H 'Authorization: Basic YW5Adm51LmVkdS52bjpjb3JyZWN0IGhvcnNlIGJhdHRlcnkgc3RhcGxl'
```

Response:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 49
Connection: close

{"orders":["o-001"],"principal":"an@vnu.edu.vn"}
```

# Lab 2:

## 1. Không gửi header X-Api-Key

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/reports
```

Response:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 16
Connection: close

{"e":"missing"}
```

## 2. API key không hợp lệ

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/reports -H 'X-Api-Key: invalid-key'
```

Response:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 16
Connection: close

{"e":"invalid"}
```

## 3. KEY1 đọc báo cáo

Request:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/reports -H 'X-Api-Key: sk_test_vXU5-ZQDjw1bY-ptdRl28sRWQc4ew3bBYLifIo1iy1M_c381d58a'
```

Response:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 58
Connection: close

{"data":"Báo cáo doanh thu tháng này","owner_id":101}
```

## 4. KEY1 thiếu scope payments:write

Request:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/pay -H 'X-Api-Key: sk_test_vXU5-ZQDjw1bY-ptdRl28sRWQc4ew3bBYLifIo1iy1M_c381d58a'
```

Response:

```http
HTTP/1.0 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 14
Connection: close

{"e":"scope"}
```

## 5. KEY2 thanh toán thành công

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/pay -H 'X-Api-Key: sk_test_ac5ToLkBduLdtCSWzV-_iuyiTPyggXg7Boflc5lZhZw_4d4ed56d'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:32 GMT
Content-Type: application/json
Content-Length: 54
Connection: close

{"message":"Thanh toán thành công","owner_id":102}
```

# Lab 3:

## 1. Chưa đăng nhập

Request đã chạy:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders
```

Response thực tế:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 39
Connection: close

{"msg":"Missing Authorization Header"}
```

## 2. Đăng nhập sai mật khẩu

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"an@vnu.edu.vn","password":"wrongpassword"}'
```

Response thực tế:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 32
Connection: close

{"error":"invalid_credentials"}
```

## 3. Đăng nhập nhận access token và refresh token

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"an@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 802
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiM2U5OTQxODUtYzAzMy00YTFiLTg5MWItMDAyZTk1NGFjYzlkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiIwNGIyYmZjNy0wNzQ3LTQ2MTctOWRkMS0xMGZjZDExZjMzN2QiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCJdfQ.hLClDe-T3XsEnovRkKGU9HaMBp3pMPibjzmh8AQD_Pw","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiNzFkMzNlMTctYWM3OC00YTEwLTgzZTYtZjgyMTQwNjFjOTc2IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzkzMDg5NzEzLCJjc3JmIjoiZmE1YWQ4ZjgtZmMxNi00OTBiLThhZTctMTAwZWM2N2JkMmJlIiwiZXhwIjoxNzk1NjgxNzEzLCJyb2xlcyI6WyJjdXN0b21lciJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiXX0.evBsbcH9uDL25L3UBzVpz-whM1b6a7hpVvkOGapKK2g"}
```

## 4. Dùng access token đọc đơn hàng của mình

Request đã chạy:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiM2U5OTQxODUtYzAzMy00YTFiLTg5MWItMDAyZTk1NGFjYzlkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiIwNGIyYmZjNy0wNzQ3LTQ2MTctOWRkMS0xMGZjZDExZjMzN2QiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCJdfQ.hLClDe-T3XsEnovRkKGU9HaMBp3pMPibjzmh8AQD_Pw'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 42
Connection: close

[{"id":101,"item":"Book A","owner_id":1}]
```

## 5. Dùng refresh token lấy access token mới

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/refresh -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiNzFkMzNlMTctYWM3OC00YTEwLTgzZTYtZjgyMTQwNjFjOTc2IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzkzMDg5NzEzLCJjc3JmIjoiZmE1YWQ4ZjgtZmMxNi00OTBiLThhZTctMTAwZWM2N2JkMmJlIiwiZXhwIjoxNzk1NjgxNzEzLCJyb2xlcyI6WyJjdXN0b21lciJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiXX0.evBsbcH9uDL25L3UBzVpz-whM1b6a7hpVvkOGapKK2g'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 401
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiODg2ZGM2NDktYTJiZS00ZjJhLTlkMGItOThkN2MwZDQ4NDI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiI1ZDRhZTI0My05OGMyLTQ1ZWEtOGQ4OS1iYjJhNmFjNTM1MmQiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCJdfQ.gURA3uUr5qkR-MrF4nxQddaR1XiRaJhBTYTEA4o2VjA"}
```

## 6. Gửi nhầm access token đến API refresh

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/refresh -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiM2U5OTQxODUtYzAzMy00YTFiLTg5MWItMDAyZTk1NGFjYzlkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiIwNGIyYmZjNy0wNzQ3LTQ2MTctOWRkMS0xMGZjZDExZjMzN2QiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCJdfQ.hLClDe-T3XsEnovRkKGU9HaMBp3pMPibjzmh8AQD_Pw'
```

Response thực tế:

```http
HTTP/1.0 422 UNPROCESSABLE ENTITY
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 42
Connection: close

{"msg":"Only refresh tokens are allowed"}
```

## 7. Gửi nhầm refresh token để đọc đơn hàng

Request đã chạy:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiNzFkMzNlMTctYWM3OC00YTEwLTgzZTYtZjgyMTQwNjFjOTc2IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzkzMDg5NzEzLCJjc3JmIjoiZmE1YWQ4ZjgtZmMxNi00OTBiLThhZTctMTAwZWM2N2JkMmJlIiwiZXhwIjoxNzk1NjgxNzEzLCJyb2xlcyI6WyJjdXN0b21lciJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiXX0.evBsbcH9uDL25L3UBzVpz-whM1b6a7hpVvkOGapKK2g'
```

Response thực tế:

```http
HTTP/1.0 422 UNPROCESSABLE ENTITY
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 46
Connection: close

{"msg":"Only non-refresh tokens are allowed"}
```

## 8. Đăng nhập dung@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"dung@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 767
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiYzQ1NTM2YjktNzk3Zi00OTc4LWE1NTMtMDIyNmM2ZjlkYTY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiI3NjNhNTE4MC1hMGE5LTQ3ZTYtYTQ5My05ZWE2YjRmYjJkMDYiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6W119.VS7RpyvGZP7YL2vqU9VBTGJx-psGwkz3_ZozaGVoa1g","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiZTAwMDg1ZjktYjIxNi00MzVlLTkwZmEtZmYzYzUwYjE0MTcxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIyIiwibmJmIjoxNzkzMDg5NzEzLCJjc3JmIjoiMzRkNDMzZTEtZDFlOS00OGM0LTkzOTItZDk3YTVjMDQ3ZjkyIiwiZXhwIjoxNzk1NjgxNzEzLCJyb2xlcyI6WyJjdXN0b21lciJdLCJzY29wZXMiOltdfQ.FsoyB26iQ2-l1PMsFkJA0sXIf3-apLCmJVM2xOmtQ9k"}
```

## 9. Người dùng thiếu scope orders:read

Request đã chạy:

```bash
curl -k -i -sS -X GET https://127.0.0.1:5443/api/orders -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxMywianRpIjoiYzQ1NTM2YjktNzk3Zi00OTc4LWE1NTMtMDIyNmM2ZjlkYTY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3OTMwODk3MTMsImNzcmYiOiI3NjNhNTE4MC1hMGE5LTQ3ZTYtYTQ5My05ZWE2YjRmYjJkMDYiLCJleHAiOjE3OTMwOTA2MTMsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6W119.VS7RpyvGZP7YL2vqU9VBTGJx-psGwkz3_ZozaGVoa1g'
```

Response thực tế:

```http
HTTP/1.0 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:33 GMT
Content-Type: application/json
Content-Length: 31
Connection: close

{"error":"insufficient_scope"}
```

# Lab 4:

## 1. Đăng nhập an@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"an@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:35 GMT
Content-Type: application/json
Content-Length: 839
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOWQ0ZTU2NTUtOWJlNi00OGY1LTlmY2MtZTA1NWFmZjY3MDNjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJjMDRkZmRiMi1jNjRkLTQzNzgtOTQ5Yi04YjFhYTgxZDJiZmEiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.QXIERPFKqJaRL5B29dUspUN9Ib4q2_iAaiT9YIySlnI","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiZmJkNGY4ZGYtY2YwYS00M2Q0LWIzM2YtZjZmZTliZjcxZWFhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzkzMDg5NzE1LCJjc3JmIjoiNDZhM2JlNjQtMDViMS00ZTg1LTg3ODctM2Y4YzU4NGQxZjcwIiwiZXhwIjoxNzk1NjgxNzE1LCJyb2xlcyI6WyJtYW5hZ2VyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCIsIm9yZGVyczp3cml0ZSJdfQ.kUSHuTZ32jg5hzByTagBx3REAJK_iOPXckAXtX1oBz0"}
```

## 2. Đăng nhập dung@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"dung@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:35 GMT
Content-Type: application/json
Content-Length: 839
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiYjRjNjU1OTctNjk5ZC00MGY4LWJjMDctMTNjYjk3NThjMDkxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiI3ZGE1NmQ4NS1lY2FiLTQ0ZDAtOWEzZC00OGE4YWUxOTEwZmYiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19._UDlF349Lu3tLt_oiKACM8ozN_4aa8T6QWZ8vIRs7_8","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiY2VlZmFjMDUtNjBlMi00MzVhLWE1NTAtN2RhMTdiYWRlYmJjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIyIiwibmJmIjoxNzkzMDg5NzE1LCJjc3JmIjoiNjAxMDViM2MtY2ExNy00ZTU2LWFmNTItNmM0YjJkMWQyYzUxIiwiZXhwIjoxNzk1NjgxNzE1LCJyb2xlcyI6WyJtYW5hZ2VyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCIsIm9yZGVyczp3cml0ZSJdfQ.D2YqHr3h0iQ8gWSc19dyA1LF1aQmPiO4JhlzlziyCAI"}
```

## 3. Đăng nhập viewer@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"viewer@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:35 GMT
Content-Type: application/json
Content-Length: 796
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOTRmNTMwN2QtYWIyNy00MzlkLTkxOWYtZmE0MDMzMDQ2YjkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjMiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJlYzlmZDRlOC1iNzE0LTQ2MzYtOGI1ZC1hYjViYzdmZWFiNDciLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbInZpZXdlciJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiXX0.aJ0RfqrjPLg41R7owYKjuNdgoFEDu3LYDepjhW1Poz0","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiYTc3ZjlkMjQtNjgwYi00OTQ1LTk4NDQtNzcxZmQyY2FkMjA3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIzIiwibmJmIjoxNzkzMDg5NzE1LCJjc3JmIjoiZDVlM2UwZDUtZGE4Ni00NDM3LTkzN2UtZDU5NDdiM2RmNzMyIiwiZXhwIjoxNzk1NjgxNzE1LCJyb2xlcyI6WyJ2aWV3ZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIl19.ZSc9ULGlkd77mxkWgTWUHlhmYafgc86lJNcD6Opx50Y"}
```

## 4. Đăng nhập limited@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"limited@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 799
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiY2Y3YTQ2ZjUtZWI5Zi00NmFkLWE5NWYtYjJiZmYzMzJjZjY5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3OTMwODk3MTYsImNzcmYiOiI1OGE4NzU3ZS1kMTRhLTRhMmMtOThkNS1jYjYyY2FhZDExMjEiLCJleHAiOjE3OTMwOTA2MTYsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIl19.fW-UA8inB0uEZbUiPXbcAGki7hQ96WozDsLriG88Pxg","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiNjM4OGM3MDYtNWRhZC00MDRkLWFhNDYtZjM4YTMyNDhjYTk1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI0IiwibmJmIjoxNzkzMDg5NzE2LCJjc3JmIjoiNzVkZmZhMDgtOGJkNC00NGQ5LWFiZmItMTFiNWI5YzZhMDg1IiwiZXhwIjoxNzk1NjgxNzE2LCJyb2xlcyI6WyJtYW5hZ2VyIl0sInNjb3BlcyI6WyJvcmRlcnM6cmVhZCJdfQ.cUTrRRw3F4Yg4sq4m5a01I0UCC-g8o2hzp-bzYUntWI"}
```

## 5. Đăng nhập admin@vnu.edu.vn

Request đã chạy:

```bash
curl -k -i -sS -X POST https://127.0.0.1:5443/api/auth/login -H 'Content-Type: application/json' -d '{"email":"admin@vnu.edu.vn","password":"secret123"}'
```

Response thực tế:

```http
HTTP/1.0 200 OK
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 836
Connection: close

{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiYTg2MjUxOGItODg2Yy00OWVjLThlZGEtZWMzMDI5YzQwNDhjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijk5IiwibmJmIjoxNzkzMDg5NzE2LCJjc3JmIjoiMzRiYTdjN2UtZDRjNC00ODZhLWEyMzgtYTdkYmY0Yjk5MjMxIiwiZXhwIjoxNzkzMDkwNjE2LCJyb2xlcyI6WyJhZG1pbiJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiLCJvcmRlcnM6d3JpdGUiXX0.wxD3T3CQ22_8kN0HJgdBtkHUIIwQySQCAaHecpYV1F4","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiZDY4YWRjNjUtMjE3Ni00NTNiLTgyNTktZTJiYTAwMjgxYWMyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI5OSIsIm5iZiI6MTc5MzA4OTcxNiwiY3NyZiI6ImViNzM2NWQ1LTg0YTAtNDJiMS1iNGU3LTMxNGQyMDY5OWEyYSIsImV4cCI6MTc5NTY4MTcxNiwicm9sZXMiOlsiYWRtaW4iXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.Jv6D6uRlZpAJp0u7AIgTO4RHA9vmIDRaPFEYxLQEmhE"}
```

## 6. Không gửi access token

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/101
```

Response thực tế:

```http
HTTP/1.0 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 39
Connection: close

{"msg":"Missing Authorization Header"}
```

## 7. User A xóa đơn 202 của User B

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/202 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOWQ0ZTU2NTUtOWJlNi00OGY1LTlmY2MtZTA1NWFmZjY3MDNjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJjMDRkZmRiMi1jNjRkLTQzNzgtOTQ5Yi04YjFhYTgxZDJiZmEiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.QXIERPFKqJaRL5B29dUspUN9Ib4q2_iAaiT9YIySlnI'
```

Response thực tế:

```http
HTTP/1.0 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 22
Connection: close

{"error":"forbidden"}
```

## 8. Viewer không có role được phép xóa

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/101 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOTRmNTMwN2QtYWIyNy00MzlkLTkxOWYtZmE0MDMzMDQ2YjkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjMiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJlYzlmZDRlOC1iNzE0LTQ2MzYtOGI1ZC1hYjViYzdmZWFiNDciLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbInZpZXdlciJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiXX0.aJ0RfqrjPLg41R7owYKjuNdgoFEDu3LYDepjhW1Poz0'
```

Response thực tế:

```http
HTTP/1.0 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 56
Connection: close

{"error":"forbidden","need_one_of":["admin","manager"]}
```

## 9. Manager thiếu scope orders:write

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/101 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiY2Y3YTQ2ZjUtZWI5Zi00NmFkLWE5NWYtYjJiZmYzMzJjZjY5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3OTMwODk3MTYsImNzcmYiOiI1OGE4NzU3ZS1kMTRhLTRhMmMtOThkNS1jYjYyY2FhZDExMjEiLCJleHAiOjE3OTMwOTA2MTYsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIl19.fW-UA8inB0uEZbUiPXbcAGki7hQ96WozDsLriG88Pxg'
```

Response thực tế:

```http
HTTP/1.0 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 62
Connection: close

{"error":"insufficient_scope","need_all_of":["orders:write"]}
```

## 10. Đơn hàng không tồn tại

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/999 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOWQ0ZTU2NTUtOWJlNi00OGY1LTlmY2MtZTA1NWFmZjY3MDNjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJjMDRkZmRiMi1jNjRkLTQzNzgtOTQ5Yi04YjFhYTgxZDJiZmEiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.QXIERPFKqJaRL5B29dUspUN9Ib4q2_iAaiT9YIySlnI'
```

Response thực tế:

```http
HTTP/1.0 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 11
Connection: close

{"e":"nf"}
```

## 11. User A xóa đơn 101 của mình

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/101 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOWQ0ZTU2NTUtOWJlNi00OGY1LTlmY2MtZTA1NWFmZjY3MDNjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJjMDRkZmRiMi1jNjRkLTQzNzgtOTQ5Yi04YjFhYTgxZDJiZmEiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.QXIERPFKqJaRL5B29dUspUN9Ib4q2_iAaiT9YIySlnI'
```

Response thực tế:

```http
HTTP/1.0 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: text/html; charset=utf-8
Connection: close
```

## 12. Xóa lại đơn 101

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/101 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNSwianRpIjoiOWQ0ZTU2NTUtOWJlNi00OGY1LTlmY2MtZTA1NWFmZjY3MDNjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTMwODk3MTUsImNzcmYiOiJjMDRkZmRiMi1jNjRkLTQzNzgtOTQ5Yi04YjFhYTgxZDJiZmEiLCJleHAiOjE3OTMwOTA2MTUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIl19.QXIERPFKqJaRL5B29dUspUN9Ib4q2_iAaiT9YIySlnI'
```

Response thực tế:

```http
HTTP/1.0 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: application/json
Content-Length: 11
Connection: close

{"e":"nf"}
```

## 13. Admin xóa đơn 202 của người khác

Request đã chạy:

```bash
curl -k -i -sS -X DELETE https://127.0.0.1:5443/api/orders/202 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MzA4OTcxNiwianRpIjoiYTg2MjUxOGItODg2Yy00OWVjLThlZGEtZWMzMDI5YzQwNDhjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijk5IiwibmJmIjoxNzkzMDg5NzE2LCJjc3JmIjoiMzRiYTdjN2UtZDRjNC00ODZhLWEyMzgtYTdkYmY0Yjk5MjMxIiwiZXhwIjoxNzkzMDkwNjE2LCJyb2xlcyI6WyJhZG1pbiJdLCJzY29wZXMiOlsib3JkZXJzOnJlYWQiLCJvcmRlcnM6d3JpdGUiXX0.wxD3T3CQ22_8kN0HJgdBtkHUIIwQySQCAaHecpYV1F4'
```

Response thực tế:

```http
HTTP/1.0 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.7
Date: Tue, 27 Oct 2026 08:28:36 GMT
Content-Type: text/html; charset=utf-8
Connection: close
```