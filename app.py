from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- DB INIT ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT,
        gesture TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        entered_gesture TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------



@app.route("/users")
def users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    users = c.execute("SELECT * FROM users").fetchall()

    conn.close()
    return render_template("users.html", users=users)


# ---------- ESP32 API ----------
@app.route("/api/gesture", methods=["POST"])
def receive_gesture():
    data = request.json
    entered = data.get("gesture")

    print("Received Pattern:", entered)

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Find user by gesture pattern
    user = c.execute(
        "SELECT * FROM users WHERE gesture=?",
        (entered,)
    ).fetchone()

    if user:
        status = "GRANTED"
        user_id = user[0]
        name = user[1]
    else:
        status = "DENIED"
        user_id = "UNKNOWN"
        name = "Unknown"

    # Save log
    c.execute(
        "INSERT INTO logs (user_id, entered_gesture, status, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, entered, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": status,
        "user": name
    })


# ---------- FETCH LOGS (LIVE) ----------
@app.route("/api/logs")
def get_logs():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    logs = c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 10").fetchall()

    conn.close()

    data = []
    for log in logs:
        data.append({
            "user_id": log[1],
            "gesture": log[2],
            "status": log[3],
            "time": log[4]
        })

    return jsonify(data)


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO users (id, name, role, gesture, status) VALUES (?, ?, ?, ?, ?)",
        (data["id"], data["name"], data["role"], data["gesture"], data["status"])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/edit_user", methods=["POST"])
def edit_user():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET name=?, role=?, gesture=?, status=?
        WHERE id=?
    """, (
        data["name"],
        data["role"],
        data["gesture"],
        data["status"],
        data["id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "updated"})

@app.route("/")
def dashboard():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    offset = (page - 1) * per_page

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    logs = c.execute(
        "SELECT * FROM logs ORDER BY id DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    ).fetchall()

    total = c.execute("SELECT COUNT(*) FROM logs").fetchone()[0]

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "dashboard.html",
        logs=logs,
        page=page,
        total_pages=total_pages
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)