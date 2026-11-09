from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "price_cents": self.price_cents
        }


def list_products():
    rows = db.session.execute(
        db.select(Product).order_by(Product.id)
    ).scalars().all()
    return [p.to_dict() for p in rows], 200


def create_product(body):
    p = Product(**body)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "sku_already_exists"}, 409
    return p.to_dict(), 201


def get_product(id):
    p = db.session.get(Product, id)
    if p is None:
        return {"error": "not_found"}, 404

    return p.to_dict(), 200
