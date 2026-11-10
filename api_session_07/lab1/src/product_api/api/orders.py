
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models.product import Product
from ..models.order import Order, OrderItem
from .schemas import OrderIn


orders_bp = Blueprint(
    "orders", __name__, url_prefix="/api/v1/orders"
)


@orders_bp.post("")
def create_order():
    try:
        body = OrderIn().load(
            request.get_json(silent=True) or {}
        )
    except ValidationError as err:
        return jsonify({
            "error": "validation_error",
            "detail": err.messages
        }), 422

    order = Order()

    for item in body["items"]:
        product = db.session.get(
            Product, item["product_id"]
        )

        if product is None or product.archived:
            db.session.rollback()
            return jsonify({
                "error": "not_found",
                "detail": "Product not found"
            }), 404

        order.items.append(
            OrderItem(
                product=product,
                qty=item["qty"]
            )
        )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "id": order.id,
        "items": [
            {
                "product_id": item["product_id"],
                "qty": item["qty"]
            }
            for item in body["items"]
        ]
    }), 201


@orders_bp.get("/<int:id>")
def get_order(id):
    stmt = db.select(Order).options(
        selectinload(Order.items).selectinload(
            OrderItem.product
        )
    ).where(Order.id == id)

    order = db.session.execute(
        stmt
    ).scalar_one_or_none()

    if order is None:
        return jsonify({
            "error": "not_found",
            "detail": "Order not found"
        }), 404

    return jsonify({
        "id": order.id,
        "items": [
            {
                "product_id": item.product_id,
                "name": item.product.name,
                "qty": item.qty
            }
            for item in order.items
        ]
    }), 200
