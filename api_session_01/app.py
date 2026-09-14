from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

STUDENTS = []
BOOKS = [
    {"id": 1, "t": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "t": "API Design Patterns", "author": "JJ Geewax"},
    {"id": 3, "t": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"},
    {"id": 4, "t": "Python Crash Course", "author": "Eric Matthes"},
    {"id": 5, "t": "Fluent Python", "author": "Luciano Ramalho"}
]

def find_by_id(book_id):
    return next((b for b in BOOKS if b["id"] == book_id), None)

@app.route("/")
def index():
    return {"message": "Hello, API!"}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 200

@app.route("/students", methods=["POST"])
def create_student():
    body = request.get_json(silent=True)
    name = body.get("name")
    if not name:
        return jsonify({"error": "name là bắt buộc"}), 400
    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa" : body.get("gpa", 0.0),
    }
    STUDENTS.append(student)
    return {"id": student["id"], "name": student["name"]}, 201

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    if not book:
        return jsonify({"error":"Not found"}), 404
    return jsonify(book), 200

@app.route("/books", methods=["GET"])
def list_books():
    limit = request.args.get("limit", 20, type=int)
    q = request.args.get("q", "").strip().lower()
    items = [b for b in BOOKS if q in b["t"].lower()]
    l_items = items[:limit]
    return jsonify({"items": l_items}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

