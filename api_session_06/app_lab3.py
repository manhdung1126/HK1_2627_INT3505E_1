from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
import bcrypt
import sqlite3

app = Flask(__name__)
app.config.update(
    SECRET_KEY="flask-secret-key-for-b6-lab-only-2026",
    JWT_SECRET_KEY="jwt-secret-key-for-b6-lab-only-2026",
    JWT_ACCESS_TOKEN_EXPIRES=900,
    JWT_REFRESH_TOKEN_EXPIRES=2592000,
    JWT_ALGORITHM="HS256"
)
jwt = JWTManager(app)

conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.row_factory = sqlite3.Row

conn.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        pwd_hash BLOB
    )
""")

conn.executemany(
    "INSERT INTO users VALUES (?, ?, ?)",
    [
        (
            1,
            "an@vnu.edu.vn",
            bcrypt.hashpw(b"secret123", bcrypt.gensalt())
        ),
        (
            2,
            "dung@vnu.edu.vn",
            bcrypt.hashpw(b"secret123", bcrypt.gensalt())
        )
    ]
)
conn.commit()

class Database:
    def fetchone(self, sql, params):
        return conn.execute(sql, params).fetchone()


db = Database()

permissions = {
    1: {"roles": ["customer"], "scopes": ["orders:read"]},
    2: {"roles": ["customer"], "scopes": []}
}

orders = [
    {"id": 101, "owner_id": 1, "item": "Book A"},
    {"id": 202, "owner_id": 2, "item": "Book B"}
]


def load_permissions(user_id):
    return permissions[int(user_id)]


def orders_by_owner(user_id):
    result = []
    for order in orders:
        if str(order["owner_id"]) == str(user_id):
            result.append(order)
    return result

redis = {}

@jwt.token_in_blocklist_loader
def check_revoked(_h, claims):
    jti = claims["jti"]
    return redis.get(
        f"revoked:{jti}"
    ) is not None

@app.post("/api/auth/login")
def login():
    user = db.fetchone(
        "SELECT id, pwd_hash FROM users WHERE email=?",
        (request.json.get("email"),))
    pwd = request.json.get("password", "").encode()
    if not user or not bcrypt.checkpw(pwd, user["pwd_hash"]):
        return jsonify(error="invalid_credentials"), 401

    claims = load_permissions(user["id"])
    uid = str(user["id"])
    return jsonify(
        access=create_access_token(
            identity=uid, additional_claims=claims),
        refresh=create_refresh_token(
            identity=uid, additional_claims=claims)
    )

@app.get("/api/orders")
@jwt_required()
def list_orders():
    uid = get_jwt_identity()
    claims = get_jwt()
    if "orders:read" not in claims.get("scopes", []):
        return jsonify(error="insufficient_scope"), 403
    return jsonify(orders_by_owner(uid))


@app.post("/api/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    claims = load_permissions(get_jwt_identity())
    return jsonify(access=create_access_token(
        identity=get_jwt_identity(), additional_claims=claims))

if __name__ == "__main__":
    app.run(ssl_context="adhoc")