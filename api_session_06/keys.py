import secrets, hashlib
from functools import wraps
from flask import request, jsonify, g
import sqlite3
from datetime import datetime, timezone

conn = sqlite3.connect("api_keys.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

class Database:
    def fetchone(self, sql, params):
        return conn.execute(sql, params).fetchone()

db = Database()

def init_db():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefix TEXT,
            hash TEXT NOT NULL UNIQUE,
            last4 TEXT,
            owner_id INTEGER,
            scopes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NULL,
            revoked_at TIMESTAMP NULL,
            ip_allowlist TEXT
        )
    """)
    conn.commit()


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def mint_key(prefix):
    raw = secrets.token_urlsafe(32)
    body = raw
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8]
    plain = f"{prefix}_{body}_{digest}"
    store = hashlib.sha256(plain.encode()).hexdigest()
    return plain, store


def create_key(prefix, owner_id, scopes):
    plain, store = mint_key(prefix)

    conn.execute(
        """
        INSERT INTO api_keys (prefix, hash, last4, owner_id, scopes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (prefix, store, plain[-4:], owner_id, ",".join(scopes))
    )
    conn.commit()
    return plain

def require_api_key(scopes=None):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            key = request.headers.get("X-Api-Key", "")
            if not key:
                return jsonify({"e": "missing"}), 401

            hashed = hashlib.sha256(key.encode()).hexdigest()
            row = db.fetchone(
                "SELECT id, owner_id, scopes, revoked_at, expires_at "
                "FROM api_keys WHERE hash=?", (hashed,))

            if (not row or row["revoked_at"] or
                (row["expires_at"] is not None and
                 row["expires_at"] <= now_utc())):
                return jsonify({"e": "invalid"}), 401

            granted = set(row["scopes"].split(","))
            if scopes and not set(scopes).issubset(granted):
                return jsonify({"e": "scope"}), 403

            g.api_key_id = row["id"]
            g.owner_id = row["owner_id"]
            g.api_scopes = granted

            return fn(*a, **kw)
        return w
    return d