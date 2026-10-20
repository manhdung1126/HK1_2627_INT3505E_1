from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    slug = mapped_column(String(100), unique=True)


class BookAuthor(db.Model):
    __tablename__ = "book_authors"

    book_id = mapped_column(
        ForeignKey("books.id"),
        primary_key=True,
    )
    author_id = mapped_column(
        ForeignKey("authors.id"),
        primary_key=True,
    )


class Book(db.Model):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(200))
    isbn = mapped_column(String(13), unique=True)
    price_vnd = mapped_column(Integer)
    stock = mapped_column(Integer, default=0)

    category_id = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category")

    authors = relationship(
        "Author",
        secondary="book_authors",
        back_populates="books",
    )

    reviews = relationship("Review", back_populates="book")

    def to_dict(self):
        return {
            "id": f"book_{self.id}",
            "title": self.title,
            "isbn": self.isbn,
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "category_id": self.category_id,
        }


class Author(db.Model):
    __tablename__ = "authors"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    bio = mapped_column(Text)
    books = relationship(
        "Book",
        secondary="book_authors",
        back_populates="authors",
    )

class User(db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(200), unique=True)
    display_name = mapped_column(String(100))
    reviews = relationship("Review", back_populates="user")


class Review(db.Model):
    __tablename__ = "reviews"

    id = mapped_column(Integer, primary_key=True)
    rating = mapped_column(Integer)

    book_id = mapped_column(ForeignKey("books.id"))
    user_id = mapped_column(ForeignKey("users.id"))
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")