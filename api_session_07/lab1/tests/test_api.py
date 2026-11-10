import pytest
from product_api.factory import create_app
from product_api.extensions import db
from product_api.models.product import Product
from product_api.models.order import Order, OrderItem


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_create_product(client):
    response = client.post("/api/v1/products", json={
        "sku": "P001",
        "name": "Laptop",
        "price_cents": 15000000,
        "qty_in_stock": 10
    })

    assert response.status_code == 201
    assert response.json["name"] == "Laptop"


def test_get_order(client):
    p1 = Product(
        sku="P001", name="Laptop", price_cents=15000000
    )
    p2 = Product(
        sku="P002", name="Mouse", price_cents=200000
    )

    order = Order(items=[
        OrderItem(product=p1, qty=1),
        OrderItem(product=p2, qty=2)
    ])

    db.session.add(order)
    db.session.commit()

    response = client.get(f"/api/v1/orders/{order.id}")

    assert response.status_code == 200
    assert len(response.json["items"]) == 2
