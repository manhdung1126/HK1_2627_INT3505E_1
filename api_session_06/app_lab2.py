from flask import Flask, jsonify, g
from keys import init_db, create_key, require_api_key

app = Flask(__name__)
app.json.ensure_ascii = False


@app.get("/api/reports")
@require_api_key(scopes=["reports:read"])
def get_reports():
    return jsonify({
        "data": "Báo cáo doanh thu tháng này",
        "owner_id": g.owner_id
    })


@app.post("/api/pay")
@require_api_key(scopes=["payments:write"])
def make_payment():
    return jsonify({
        "message": "Thanh toán thành công",
        "owner_id": g.owner_id
    })


if __name__ == "__main__":
    init_db()
    key_readonly = create_key("sk_test", 101, ["reports:read"])
    key_full = create_key("sk_test", 102, ["reports:read", "payments:write"])

    print("KEY1 =", key_readonly)
    print("KEY2 =", key_full)

    app.run(ssl_context="adhoc")