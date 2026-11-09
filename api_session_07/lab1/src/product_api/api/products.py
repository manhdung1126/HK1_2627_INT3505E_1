from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from ..extensions import db
from ..models.product import Product
from .schemas import ProductOut, ProductIn, ProductPatch, ReserveIn

products_bp = Blueprint(
    "products", __name__, url_prefix="/api/v1/products"
)


@products_bp.errorhandler(ValidationError)
def validation_error(err):
    return jsonify({
        "error": "validation_error",
        "detail": err.messages
    }), 422


@products_bp.errorhandler(404)
def not_found(err):
    return jsonify({
        "error": "not_found",
        "detail": "Product not found"
    }), 404


@products_bp.get("")
def list_products():
    try:
        page = max(1, int(request.args.get("page", 1)))
        size = min(100, max(1,
            int(request.args.get("size", 20))))
    except ValueError:
        return jsonify({
            "error": "validation_error",
            "detail": "page and size must be integers"
        }), 422

    base = db.select(Product).where(
        Product.archived.is_(False))

    rows = db.session.execute(
        base.order_by(Product.id)
        .offset((page - 1) * size).limit(size)
    ).scalars().all()

    return jsonify({
        "items": [ProductOut().dump(p) for p in rows],
        "page": page,
        "size": size,
        "total": db.session.scalar(
            db.select(db.func.count())
            .select_from(Product)
            .where(Product.archived.is_(False))
        )
    }), 200


@products_bp.get("/<int:id>")
def get_product(id):
    p = db.get_or_404(Product, id)

    if p.archived:
        return jsonify({
            "error": "not_found",
            "detail": "Product not found"
        }), 404

    return ProductOut().dump(p), 200


@products_bp.post("")
def create_product():
    body = ProductIn().load(
        request.get_json(silent=True) or {}
    )

    p = Product(**body)
    db.session.add(p)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "conflict",
            "detail": "sku already exists"
        }), 409

    return ProductOut().dump(p), 201


@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    body = ReserveIn().load(
        request.get_json(silent=True) or {}
    )

    p = db.get_or_404(Product, id)

    if p.archived:
        return jsonify({
            "error": "not_found",
            "detail": "Product not found"
        }), 404

    qty = body["qty"]

    if p.qty_in_stock < qty:
        return jsonify({
            "error": "conflict",
            "detail": "Not enough stock"
        }), 409

    p.qty_in_stock -= qty
    db.session.commit()

    return ProductOut().dump(p), 200


@products_bp.patch("/<int:id>")
def patch_product(id):
    body = ProductPatch().load(
        request.get_json(silent=True) or {},
        partial=True
    )

    p = db.get_or_404(Product, id)

    if p.archived:
        return jsonify({
            "error": "not_found",
            "detail": "Product not found"
        }), 404

    for k, v in body.items():
        setattr(p, k, v)

    db.session.commit()
    return ProductOut().dump(p), 200


@products_bp.delete("/<int:id>")
def delete_product(id):
    p = db.get_or_404(Product, id)

    if p.archived:
        return jsonify({
            "error": "not_found",
            "detail": "Product not found"
        }), 404

    p.archived = True
    db.session.commit()

    return "", 204
