from flask import Flask, jsonify, request, make_response
import sqlite3

app = Flask(__name__)
DEFAULT_SIZE, MAX_SIZE = 20, 100

def init_db():
    db = sqlite3.connect("books.db")

    db.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            price REAL
        )
    """)

    db.commit()
    db.close()

init_db()

def get_db():
    db = sqlite3.connect("books.db")
    db.row_factory = sqlite3.Row
    return db

@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)
    db = get_db()
    fit = []
    for row in db.execute("SELECT * FROM books").fetchall():
        fit.append(dict(row))
    db.close()
    a = request.args.get("author")
    if a:
        fit = [b for b in fit if b["author"].lower() == a.lower()]
    q = (request.args.get("q") or "").lower()
    if q:
        fit = [b for b in fit if q in b["title"].lower()]
    total = len(fit)
    start = (page-1)*size; end = start+size
    items = fit[start:end]
    last = (total+size-1) // size

    def u(p):
        return f"/books?page={p}&size={size}"

    links = {"self":{"href": u(page)}, "first":{"href": u(1)}, "last":{"href": u(max(1, last))}}
    if page > 1: links["prev"] = {"href": u(page-1)}
    if end < total: links["next"] = {"href": u(page+1)}
    body = {"data":items, "pagination":{"page":page,"size":size,"total":total,"total_pages":last},"_links":links}
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp

@app.post("/books")
def create_book():
    if not request.is_json:
        return jsonify(error="expected JSON"), 415
    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()
    if not a or not t:
        return jsonify(error = "title and author required"), 422
    db = get_db()
    cursor = db.execute("INSERT INTO books (title, author, isbn, price) VALUES (?, ?, ?, ?)", (t, a, p.get("isbn"), p.get("price")))
    db.commit()
    book_id = cursor.lastrowid
    db.close()
    resp = make_response(jsonify({"id": book_id, "title": t, "author": a, "isbn": p.get("isbn"), "price": p.get("price")}), 201)
    resp.headers["Location"] = f"/books/{book_id}"
    return resp

@app.get("/books/<int:bid>")
def fetch(bid):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    db.close()
    if row is None:
        return jsonify(error="not found"), 404
    resp = make_response(jsonify(dict(row)), 200)
    resp.headers["Cache-Control"] = "max-age=60"; return resp

@app.put("/books/<int:bid>")
def put(bid):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    if row is None:
        db.close()
        return jsonify(error="not found"), 404
    p = request.get_json(silent=True) or {}
    t = p.get("title")
    a = p.get("author")
    if not a or not t:
        db.close()
        return jsonify(error = "need title + author"), 422
    cursor = db.execute("UPDATE books SET title = ?, author = ?, isbn = ?, price = ? WHERE id = ?", (t.strip(), a.strip(), p.get("isbn"), p.get("price"), bid))
    db.commit()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    db.close()
    return jsonify(dict(row)), 200

@app.patch("/books/<int:bid>")
def patch(bid):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    if row is None:
        db.close()
        return jsonify(error="not found"), 404
    p = request.get_json(silent=True) or {}
    if p.get("price", 0) < 0:
        db.close()
        return jsonify(error = "price must be positive"), 422
    for k in "title author isbn price".split():
        if k in p:
            db.execute("UPDATE books SET {} = ? WHERE id = ?".format(k), (p[k], bid))
    db.commit()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    db.close()
    return jsonify(dict(row)), 200

@app.delete("/books/<int:bid>")
def delete(bid):
    db = get_db()
    cursor = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    if cursor is None:
        db.close()
        return jsonify(error="not found"), 404
    db.execute("DELETE FROM books WHERE id = ?", (bid,))
    db.commit()
    db.close()
    return "", 204
