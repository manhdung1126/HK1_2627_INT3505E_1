## 1. Phân trang Offset + Filter genre + Multi-key Sort

Lấy sách thuộc thể loại `tech`, sắp xếp theo giá giảm dần, trùng giá thì tên tăng dần:

```bash
curl -i "http://localhost:5000/api/v1/books?strategy=offset&genre=tech&sort=-price,title&offset=0&limit=1"
```

Kết quả: `200 OK`

```json
{
  "data": [
    {
      "id": "book_2",
      "title": "Refactoring",
      "isbn": "9780201485677",
      "price_vnd": 500000,
      "stock": 5,
      "category_id": 1
    }
  ],
  "page": {
    "strategy": "offset",
    "next": null,
    "next_offset": 1,
    "more": true
  }
}
```

Lấy trang tiếp theo:

```bash
curl -i "http://localhost:5000/api/v1/books?strategy=offset&genre=tech&sort=-price,title&offset=1&limit=1"
```

Kết quả: `200 OK`

```json
{
  "data": [
    {
      "id": "book_1",
      "title": "Clean Code",
      "isbn": "9780132350884",
      "price_vnd": 450000,
      "stock": 10,
      "category_id": 1
    }
  ],
  "page": {
    "strategy": "offset",
    "next": null,
    "next_offset": null,
    "more": false
  }
}
```

## 2. Phân trang Cursor

### 2.1. Lấy trang đầu tiên

```bash
curl -i "http://localhost:5000/api/v1/books?strategy=cursor&sort=id&limit=2"
```

Kết quả: `200 OK`

Trong ví dụ, `TOKEN` đại diện cho chuỗi cursor server trả về.

```json
{
  "data": [
    {
      "id": "book_1",
      "title": "Clean Code",
      "isbn": "9780132350884",
      "price_vnd": 450000,
      "stock": 10,
      "category_id": 1
    },
    {
      "id": "book_2",
      "title": "Refactoring",
      "isbn": "9780201485677",
      "price_vnd": 500000,
      "stock": 5,
      "category_id": 1
    }
  ],
  "page": {
    "strategy": "cursor",
    "next": "TOKEN",
    "next_offset": null,
    "more": true
  }
}
```

### 2.2. Lấy trang tiếp theo

```bash
curl -i -G "http://localhost:5000/api/v1/books" \
  --data-urlencode "strategy=cursor" \
  --data-urlencode "sort=id" \
  --data-urlencode "limit=2" \
  --data-urlencode "cursor=TOKEN"
```

Kết quả: `200 OK`

Ví dụ khi database chỉ có ba sách:

```json
{
  "data": [
    {
      "id": "book_3",
      "title": "The Martian",
      "isbn": "9780553418026",
      "price_vnd": 180000,
      "stock": 20,
      "category_id": 2
    }
  ],
  "page": {
    "strategy": "cursor",
    "next": null,
    "next_offset": null,
    "more": false
  }
}
```

## 3. READ — Xem chi tiết sách

```bash
curl -i "http://localhost:5000/api/v1/books/1"
```

Kết quả: `200 OK`

```json
{
  "id": "book_1",
  "title": "Clean Code",
  "isbn": "9780132350884",
  "price_vnd": 450000,
  "stock": 10,
  "category_id": 1
}
```

## 4. CREATE — Tạo sách hợp lệ

```bash
curl -i -X POST "http://localhost:5000/api/v1/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python cơ bản",
    "isbn": "9780000000095",
    "price_vnd": 150000,
    "stock": 8,
    "category_id": 1
  }'
```

Kết quả: `201 Created`

Ví dụ sách mới có ID 4:

```json
{
  "id": "book_4",
  "title": "Python cơ bản",
  "isbn": "9780000000095",
  "price_vnd": 150000,
  "stock": 8,
  "category_id": 1
}
```

## 5. Kiểm tra JSON Schema Validation


```bash
curl -i -X POST "http://localhost:5000/api/v1/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Invalid Book",
    "isbn": "9780000000096",
    "price_vnd": -5000,
    "stock": 1,
    "category_id": 1
  }'
```

Kết quả: `400 Bad Request`

```json
{
  "error": "-5000 is less than the minimum of 0"
}
```

## 6. UPDATE — Cập nhật sách


```bash
curl -i -X PATCH "http://localhost:5000/api/v1/books/4" \
  -H "Content-Type: application/json" \
  -d '{
    "price_vnd": 170000,
    "stock": 0
  }'
```

Kết quả: `200 OK`

```json
{
  "id": "book_4",
  "title": "Python cơ bản",
  "isbn": "9780000000095",
  "price_vnd": 170000,
  "stock": 0,
  "category_id": 1
}
```


```bash
curl -i "http://localhost:5000/api/v1/books/4"
```

Kết quả: `200 OK`

```json
{
  "id": "book_4",
  "title": "Python cơ bản",
  "isbn": "9780000000095",
  "price_vnd": 170000,
  "stock": 0,
  "category_id": 1
}
```

## 7. DELETE — Xóa sách

```bash
curl -i -X DELETE "http://localhost:5000/api/v1/books/4"
```

Kết quả: `204 No Content`, không có body.

Kiểm tra sau khi xóa:

```bash
curl -i "http://localhost:5000/api/v1/books/4"
```

Kết quả: `404 Not Found`

```json
{
  "error": "Book not found"
}
```

## 8. Kiểm tra sort không hợp lệ

```bash
curl -i "http://localhost:5000/api/v1/books?sort=unknown"
```

Kết quả: `400 Bad Request`

```json
{
  "error": "Tham số không hợp lệ"
}
```

## 9. Kiểm tra limit không hợp lệ

```bash
curl -i "http://localhost:5000/api/v1/books?limit=0"
```

Kết quả: `400 Bad Request`

```json
{
  "error": "Limit hoặc offset không hợp lệ"
}
```

## 10. Kiểm tra cursor không hợp lệ

```bash
curl -i "http://localhost:5000/api/v1/books?strategy=cursor&cursor=abc"
```

Kết quả: `400 Bad Request`

```json
{
  "error": "Cursor không hợp lệ hoặc sort đã đổi"
}
```