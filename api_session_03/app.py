from flask import Flask, jsonify, request, make_response
from errors import ApiProblem, _problem
import base64

app = Flask(__name__)

POSTS = []
_next_post_id = 1
USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]
ORDERS = [
    {"id": 1, "customer_id": 101, "status": "paid", "total": 120},
    {"id": 2, "customer_id": 102, "status": "pending", "total": 80},
    {"id": 3, "customer_id": 101, "status": "paid", "total": 250},
    {"id": 4, "customer_id": 103, "status": "cancelled", "total": 50},
    {"id": 5, "customer_id": 102, "status": "paid", "total": 300},
    {"id": 6, "customer_id": 101, "status": "pending", "total": 90},
]

@app.get("/api/v1/posts")
def list_posts():
    return jsonify({"data": POSTS, "total": len(POSTS)}), 200

@app.post("/api/v1/posts")
def create_post():
    global _next_post_id

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    body = request.get_json(silent=True) or {}

    title = (body.get("title") or "").strip()
    content = (body.get("content") or "").strip()
    author_id = body.get("author_id")

    if not title or not content or author_id is None:
        return jsonify(error="title, content and author_id are required"), 422

    post = {
        "id": _next_post_id,
        "title": title,
        "content": content,
        "author_id": author_id,
        "tags": body.get("tags", [])
    }

    POSTS.append(post)
    _next_post_id += 1

    resp = make_response(jsonify(post), 201)
    resp.headers["Location"] = f"/api/v1/posts/{post['id']}"

    return resp

@app.errorhandler(ApiProblem)
def handle_api_problem(error):
    return _problem(
        status=error.status,
        title=error.title,
        detail=error.detail,
        type_path=None if error.type == "about:blank"
        else error.type.split("/")[-1],
        **error.extra
    )


@app.get("/users/<int:id>")
def get_user(id):
    user = next(
        (u for u in USERS if u["id"] == id),
        None
    )

    if not user:
        raise ApiProblem(
            status=404,
            title="User not found",
            type_path="user-not-found",
            resource_id=id,
        )

    return jsonify(user)

def encode_cursor(index):
    return base64.b64encode(str(index).encode()).decode()


def decode_cursor(cursor):
    try:
        return int(base64.b64decode(cursor).decode())
    except:
        return None


@app.get("/orders")
def get_orders():
    orders = ORDERS.copy()
    status = request.args.get("status")
    customer_id = request.args.get("customer_id")

    if status:
        orders = [o for o in orders if o["status"] == status]

    if customer_id:
        orders = [o for o in orders if o["customer_id"] == int(customer_id)]

    sort = request.args.get("sort")
    if sort:
        orders.sort(key=lambda o: o[sort])
    limit = int(request.args.get("limit", 5))
    cursor = request.args.get("cursor")
    start = 0

    if cursor:
        start = decode_cursor(cursor)
        if start is None:
            return jsonify(error="invalid cursor"), 400

    items = orders[start:start + limit]
    next_cursor = None
    if start + limit < len(orders):
        next_cursor = encode_cursor(start + limit)

    fields = request.args.get("fields")
    if fields:
        fields = fields.split(",")
        items = [{key: value for key, value in order.items() if key in fields} for order in items]

    return jsonify({"data": items, "next_cursor": next_cursor})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)