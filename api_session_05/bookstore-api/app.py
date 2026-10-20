from flask import Flask
from models import db, Book, Author, Category, User, Review
from routes.books import books_bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
db.init_app(app)
app.register_blueprint(books_bp)

with app.app_context():
    db.create_all()
    if db.session.scalar(db.select(Book.id).limit(1)) is None:
        tech = Category(name="Công nghệ", slug="tech")
        fiction = Category(name="Tiểu thuyết", slug="fiction")

        robert = Author(name="Robert C. Martin", bio="Software engineer")
        martin = Author(name="Martin Fowler", bio="Software engineer")
        kent = Author(name="Kent Beck", bio="Software engineer")
        andy = Author(name="Andy Weir", bio="Novelist")

        book1 = Book(
            title="Clean Code",
            isbn="9780132350884",
            price_vnd=450000,
            stock=10,
            category=tech,
            authors=[robert],
        )

        book2 = Book(
            title="Refactoring",
            isbn="9780201485677",
            price_vnd=500000,
            stock=5,
            category=tech,
            authors=[martin, kent],
        )

        book3 = Book(
            title="The Martian",
            isbn="9780553418026",
            price_vnd=180000,
            stock=20,
            category=fiction,
            authors=[andy],
        )

        dung = User(email="dung@example.com", display_name="Dũng")
        an = User(email="an@example.com", display_name="An")

        review1 = Review(rating=5, book=book1, user=dung)
        review2 = Review(rating=4, book=book1, user=an)
        review3 = Review(rating=5, book=book3, user=dung)

        db.session.add_all([
            tech, fiction,
            robert, martin, kent, andy,
            book1, book2, book3,
            dung, an,
            review1, review2, review3,
        ])

        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)