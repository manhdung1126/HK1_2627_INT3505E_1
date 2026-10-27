import bcrypt
from flask import g
from flask_jwt_extended import jwt_required
from app_lab3 import (
    app, jwt, conn, db, permissions, orders, load_permissions
)
from auth import require_roles, require_scopes, user_owns_resource

permissions.update({
    1: {
        "roles": ["manager"],
        "scopes": ["orders:read", "orders:write"]
    },
    2: {
        "roles": ["manager"],
        "scopes": ["orders:read", "orders:write"]
    },
    3: {
        "roles": ["viewer"],
        "scopes": ["orders:read"]
    },
    4: {
        "roles": ["manager"],
        "scopes": ["orders:read"]
    },
    99: {
        "roles": ["admin"],
        "scopes": ["orders:read", "orders:write"]
    }
})

pwd_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt())

conn.executemany(
    "INSERT INTO users VALUES (?, ?, ?)",
    [
        (3, "viewer@vnu.edu.vn", pwd_hash),
        (4, "limited@vnu.edu.vn", pwd_hash),
        (99, "admin@vnu.edu.vn", pwd_hash)
    ]
)

conn.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        owner_id INTEGER,
        item TEXT
    )
""")

conn.executemany(
    "INSERT INTO orders VALUES (?, ?, ?)",
    [
        (101, 1, "Book A"),
        (202, 2, "Book B")
    ]
)
conn.commit()


@jwt.user_lookup_loader
def load_current_user(_header, claims):
    user = db.fetchone(
        "SELECT id FROM users WHERE id=?",
        (claims["sub"],)
    )
    if not user:
        return None

    g.current_user = {
        "id": user["id"],
        "roles": load_permissions(user["id"])["roles"]
    }
    return g.current_user


class OrderService:
    def delete_authorized(self, id, current_user):
        conn.execute("DELETE FROM orders WHERE id=?", (id,))
        conn.commit()
    
        for order in orders:
            if order["id"] == id:
                orders.remove(order)
                break


order_svc = OrderService()

@app.delete("/api/orders/<int:id>")
@jwt_required()
@require_roles("admin", "manager")
@require_scopes("orders:write")
@user_owns_resource("id")
def delete_order(id):
    order_svc.delete_authorized(id, g.current_user)
    return "", 204


if __name__ == "__main__":
    app.run(ssl_context="adhoc")