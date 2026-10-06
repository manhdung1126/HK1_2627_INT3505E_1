from flask import Flask, jsonify, request, make_response
from errors import ApiProblem, _problem

app = Flask(__name__)

POSTS = []
_next_post_id = 1
USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)