import json
import base64
import binascii
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
from sqlalchemy import select, tuple_
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
}


def parse_sort(raw):
    desc = raw.startswith("-")
    key = raw.lstrip("-")

    if key not in SORT:
        return None, "bad_sort", 400

    p = SORT[key]
    cols = [p.desc() if desc else p.asc(),Book.id.desc() if desc else Book.id.asc()]

    return p, cols, desc

def _enc(s):
    return base64.urlsafe_b64encode(json.dumps(s).encode()).decode().rstrip("=")

def apply_cursor(q, raw, sort, p, desc):
    if not raw:
        return q, None, 200

    pad = "=" * (-len(raw) % 4)
    c = json.loads(base64.urlsafe_b64decode(raw + pad))

    if c.get("s") != sort:
        return None, "sort_chg", 400

    v, i = c["v"], c["i"]
    op = "<" if desc else ">"
    condition = tuple_(p, Book.id).op(op)((v, i))

    return q.filter(condition), None, 200


def build_response(items, lim, sort, p, more):
    nxt = None

    if items and more:
        last = items[-1]

        nxt = _enc({
            "s": sort,
            "v": getattr(last, p.key),
            "i": last.id,
        })

    return jsonify({
        "data": [b.to_dict() for b in items],
        "page": {
            "next": nxt,
            "more": more,
        },
    })

@books_bp.get("")
def list_books():
    raw = request.args.get("cursor")
    lim = min(request.args.get("limit", 20, type=int), 100)

    sort = request.args.get("sort", "-id")
    cat = request.args.get("category", type=int)

    p, cols, desc = parse_sort(sort)
    if p is None:
        return cols, 400

    q = select(Book).order_by(*cols)
    if cat:
        q = q.filter(Book.category_id == cat)

    q, err, code = apply_cursor(q, raw, sort, p, desc)
    if err:
        return {"e": err}, code

    rows = db.session.scalars(q.limit(lim + 1)).all()
    return build_response(rows[:lim], lim, sort, p, len(rows) > lim)

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

