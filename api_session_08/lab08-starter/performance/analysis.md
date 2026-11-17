# Lab 4 — Phân tích kết quả Load Test Books API

## 1. Bảng tổng hợp số liệu thực tế

| Kịch bản | Users | Spawn rate (user/s) | Duration | Requests | Failures | p95 (ms) | Failure rate | RPS | Báo cáo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 10 | 2 | 30s | 132 | 1 | 9 | 0.76% | 4.87 | [A.html](../reports/A.html) |
| B | 50 | 5 | 60s | 1404 | 1 | 12 | 0.07% | 23.51 | [B.html](../reports/B.html) |
| C | 200 | 50 | 30s | 2897 | 4 | 45 | 0.14% | 97.44 | [C.html](../reports/C.html) |

Failure rate = số request bị đánh dấu thất bại / tổng số request × 100%.

## 2. Phân tích theo yêu cầu

### Câu 1: Kịch bản nào có p95 cao nhất? Vì sao?

Kịch bản C có p95 cao nhất, bằng 45 ms, so với 9 ms của A và 12 ms của B. C tăng lên 200 users với tốc độ 50 user/s, nên đạt mức tải mục tiêu sau khoảng 4 giây. RPS tăng từ 4.87 ở A lên 97.44 ở C, đồng thời p95 tăng.

Trong C, POST /books có p95 = 54 ms, GET /books = 48 ms, GET /books?year=... = 40 ms và GET /books/{id} = 37 ms. Tải đồng thời lớn hơn có thể làm tăng thời gian chờ xử lý và truy cập cơ sở dữ liệu. Tuy nhiên, chưa đo CPU, thời gian chờ kết nối hay khóa SQLite nên chưa xác định được nút thắt cụ thể.

### Câu 2: Endpoint nào có failure rate tăng? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.

Chỉ task GET /books?year=... có failure:

| Kịch bản | Requests tìm theo năm | Failures | Failure rate của task |
|---|---:|---:|---:|
| A | 16 | 1 | 6.25% |
| B | 191 | 1 | 0.52% |
| C | 397 | 4 | 1.01% |

Failure rate không tăng đều theo số user. Task có đoạn giả lập lỗi:

```python
if response.status_code == 200 and random.random() < 0.01:
    response.failure("Simulated 500 (client-side)")
```

Server đã trả HTTP 200, sau đó Locust đánh dấu request thất bại với xác suất 1%. Vì vậy, thông báo Simulated 500 (client-side) không phải HTTP 500 thực từ API. Ba báo cáo chỉ ghi nhận loại failure này; các task còn lại có 0 failure. Riêng GET /books/{id}, mã 404 dự kiến đã được script đánh dấu thành công.

Ở A chỉ có 16 request tìm theo năm nên một failure đã tương ứng 6.25%. Tỷ lệ ngẫu nhiên quan sát được không nhất thiết bằng đúng 1%, đặc biệt khi mẫu nhỏ.

### Câu 3: Với SLO p95 < 300 ms, kịch bản nào đạt? Giới hạn phép đo và baseline cho CI.

Cả A, B và C đều đạt ngưỡng p95 < 300 ms trong các lượt đo này: lần lượt là 9, 12 và 45 ms. Các p95 theo từng endpoint trong ba báo cáo cũng đều dưới 300 ms.

Giới hạn: mỗi kịch bản mới chạy một lần trong 30–60 giây; API và Locust cùng chạy trên một máy; sử dụng Flask development server và SQLite. Dữ liệu cũng tăng sau các request tạo sách và không được đưa về cùng trạng thái giữa các lượt. Vì vậy, kết quả chưa đủ để khẳng định đáp ứng SLO ở production.

Baseline CI đề xuất là A: 10 users, spawn rate 2 user/s, 30 giây, vì nhẹ và chạy nhanh. Có thể kiểm tra p95 < 300 ms và không có lỗi vận hành ngoài dự kiến. Khi dùng failure rate làm điều kiện CI, cần tắt giả lập lỗi hoặc tách riêng Simulated 500 (client-side). Đây là đề xuất, chưa triển khai CI gate.

### Câu 4: Nếu connection pool giới hạn ở 5, kiểm chứng ảnh hưởng như thế nào?

Nếu dùng SQLAlchemy QueuePool, cần đặt pool_size=5 và max_overflow=0 để giới hạn tối đa 5 kết nối. Chỉ đặt pool_size=5 vẫn có thể cho phép mở thêm kết nối qua overflow.

Khi cả 5 kết nối đang bận, request cần truy cập cơ sở dữ liệu phải chờ; nếu vượt pool_timeout, có thể phát sinh lỗi lấy kết nối. 200 users không đồng nghĩa có 200 kết nối cơ sở dữ liệu cùng lúc, vì mỗi user còn có thời gian chờ 1–3 giây giữa các task.

Cách kiểm chứng:

1. Chạy trên cơ sở dữ liệu thử nghiệm với cùng dữ liệu ban đầu, giữ nguyên kịch bản C và tắt giả lập lỗi để dễ nhận biết lỗi thực.
2. So sánh cấu hình pool hiện tại với giới hạn 5, giữ các điều kiện còn lại giống nhau và chạy lặp lại.
3. So sánh p95, RPS, failure rate và đối chiếu log server để tìm lỗi chờ kết nối như QueuePool ... timed out.

Nếu p95 tăng, RPS bị giới hạn và log xuất hiện lỗi chờ kết nối, đó là bằng chứng pool ảnh hưởng đến kết quả. 
