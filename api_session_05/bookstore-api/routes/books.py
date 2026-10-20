from flask import Blueprint, jsonify
from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

@books_bp.get("")
def list_books():
    statement = db.select(Book).order_by(Book.id)
    books = db.session.execute(statement).scalars().all()

    return jsonify([book.to_dict() for book in books])