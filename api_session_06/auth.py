from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import get_jwt
from app_lab3 import db

def require_roles(*allowed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            urs = set(g.current_user["roles"])
            if not urs & set(allowed):
                return jsonify({
                    "error": "forbidden",
                    "need_one_of": list(allowed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


def require_scopes(*needed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            granted = set(get_jwt().get("scopes", []))
            if not set(needed).issubset(granted):
                return jsonify({
                    "error": "insufficient_scope",
                    "need_all_of": list(needed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


def user_owns_resource(param="id"):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            row = db.fetchone(
                "SELECT owner_id FROM orders WHERE id=?",
                (kw[param],))
            if not row:
                return jsonify({"e": "nf"}), 404

            ok = str(row["owner_id"]) == str(g.current_user["id"])
            if not ok and "admin" not in g.current_user["roles"]:
                return jsonify({"error": "forbidden"}), 403

            return fn(*a, **kw)
        return w
    return d