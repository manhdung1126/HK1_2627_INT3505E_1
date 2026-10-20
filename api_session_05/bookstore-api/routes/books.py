import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
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

    cols = [
        p.desc() if desc else p.asc(),
        Book.id.desc() if desc else Book.id.asc(),
    ]

    return p, cols, desc

@books_bp.get("")
def list_books():
    sort = request.args.get("sort", "-id")
    category_id = request.args.get("category", type=int)
    p, cols, desc = parse_sort(sort)
    if p is None:
        return jsonify({"error": cols}), 400
    statement = db.select(Book).order_by(*cols)

    if category_id is not None:
        statement = statement.where(
            Book.category_id == category_id
        )
    books = db.session.scalars(statement).all()
    return jsonify([book.to_dict() for book in books])

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

