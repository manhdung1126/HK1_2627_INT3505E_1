import json
import base64
import binascii
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import IntegrityError

from models import db, Book, Category, Review

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")
schema_path = (
    Path(__file__).resolve().parent.parent
    / "schemas"
    / "book.json"
)

with schema_path.open(encoding="utf-8") as file:
    book_schema = json.load(file)
    book_patch_schema = {**book_schema, "required": [], "minProperties": 1}

SORT = {
    "id": Book.id,
    "price": Book.price_vnd,
    "title": Book.title,
}


def parse_sort(raw):
    keys = []

    for field in raw.split(","):
        desc = field.startswith("-")
        name = field[1:] if desc else field

        if name not in SORT:
            raise ValueError("Sort không hợp lệ")

        keys.append((SORT[name], desc))

    if not any(p.key == "id" for p, desc in keys):
        keys.append((Book.id, False))

    return keys


def _enc(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def apply_cursor(q, raw, sort, keys):
    if not raw:
        return q

    c = json.loads(base64.urlsafe_b64decode(raw))

    if c["sort"] != sort:
        raise ValueError("Không được đổi sort khi dùng cursor")

    if len(c["values"]) != len(keys):
        raise ValueError("Cursor không hợp lệ")

    conditions = []
    equal = []

    for (p, desc), value in zip(keys, c["values"]):
        comparison = p < value if desc else p > value
        conditions.append(and_(*equal, comparison))
        equal.append(p == value)

    return q.where(or_(*conditions))


@books_bp.get("")
def list_books():
    strategy = request.args.get("strategy", "cursor")
    sort = request.args.get("sort", "-id")
    genre = request.args.get("genre")
    cursor = request.args.get("cursor")

    if strategy not in ("offset", "cursor"):
        return {"error": "Strategy không hợp lệ"}, 400

    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
        keys = parse_sort(sort)
    except ValueError:
        return {"error": "Tham số không hợp lệ"}, 400

    if limit < 1 or offset < 0:
        return {"error": "Limit hoặc offset không hợp lệ"}, 400

    limit = min(limit, 100)

    q = select(Book).order_by(*[
        p.desc() if desc else p.asc()
        for p, desc in keys
    ])

    if genre:
        q = q.join(Book.category).where(Category.slug == genre)

    if strategy == "offset":
        q = q.offset(offset)
    else:
        try:
            q = apply_cursor(q, cursor, sort, keys)
        except (ValueError, KeyError, TypeError, binascii.Error):
            return {"error": "Cursor không hợp lệ hoặc sort đã đổi"}, 400

    rows = db.session.scalars(q.limit(limit + 1)).all()
    items = rows[:limit]
    more = len(rows) > limit

    next_cursor = None
    next_offset = None

    if more:
        if strategy == "cursor":
            last = items[-1]
            next_cursor = _enc({
                "sort": sort,
                "values": [
                    getattr(last, p.key)
                    for p, desc in keys
                ],
            })
        else:
            next_offset = offset + limit

    return jsonify({
        "data": [book.to_dict() for book in items],
        "page": {
            "strategy": strategy,
            "next": next_cursor,
            "next_offset": next_offset,
            "more": more,
        },
    })

@books_bp.get("/<int:book_id>")
def get_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book.to_dict())

@books_bp.post("")
def create_book():
    if not request.is_json:
        return jsonify({"error": "Content-Type phải là application/json"}), 415

    data = request.get_json()
    try:
        validate(instance=data, schema=book_schema)
    except ValidationError as error:
        return jsonify({"error": error.message}), 400

    category = db.session.get(Category, data["category_id"])
    if category is None:
        return jsonify({"error": "Category không tồn tại"}), 400

    book = Book(
        title=data["title"],
        isbn=data["isbn"],
        price_vnd=data["price_vnd"],
        stock=data.get("stock", 0),
        category=category,
    )

    db.session.add(book)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Không thể lưu sách, kiểm tra ISBN có bị trùng không"}), 409

    return (jsonify(book.to_dict()), 201, {"Location": f"/api/v1/books/{book.id}"},)

@books_bp.patch("/<int:book_id>")
def update_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type phải là application/json"}), 415

    data = request.get_json()

    try:
        validate(instance=data, schema=book_patch_schema)
    except ValidationError as error:
        return jsonify({"error": error.message}), 400

    if "category_id" in data:
        category = db.session.get(Category, data["category_id"])

        if category is None:
            return jsonify({"error": "Category không tồn tại"}), 400
        book.category = category

    for field in ("title", "isbn", "price_vnd", "stock"):
        if field in data:
            setattr(book, field, data[field])
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Không thể cập nhật, kiểm tra ISBN có bị trùng không"}), 409

    return jsonify(book.to_dict())

@books_bp.delete("/<int:book_id>")
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    review_id = db.session.scalar(
        db.select(Review.id)
        .where(Review.book_id == book_id)
        .limit(1)
    )

    if review_id is not None:
        return jsonify({"error": "Không thể xóa sách đã có đánh giá"}), 409

    book.authors.clear()
    db.session.delete(book)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Sách còn dữ liệu liên quan"}), 409

    return "", 204

