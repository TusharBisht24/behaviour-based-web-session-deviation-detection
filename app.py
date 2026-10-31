from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB = "behaviour.db"


def connect_db():
    return sqlite3.connect(DB)


def create_tables():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            page TEXT,
            event_time TEXT,
            deviation_score INTEGER,
            status TEXT
        )
    """)

    cur.execute("SELECT id FROM users WHERE username = ?", ("student",))

    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            ("student", generate_password_hash("student123"))
        )

    con.commit()
    con.close()


def analyse_behaviour(username):
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM events
        WHERE username = ?
        AND event_time >= ?
    """, (
        username,
        datetime.fromtimestamp(time.time() - 60).strftime("%Y-%m-%d %H:%M:%S")
    ))

    recent_requests = cur.fetchone()[0]
    con.close()

    score = 0

    if recent_requests >= 10:
        score += 50

    current_hour = datetime.now().hour

    if current_hour < 6 or current_hour > 23:
        score += 30

    status = "Suspicious" if score >= 50 else "Normal"

    return score, status


def log_activity(page):
    username = session.get("username")

    if not username:
        return

    score, status = analyse_behaviour(username)

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO events
        (username, page, event_time, deviation_score, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        page,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        score,
        status
    ))

    con.commit()
    con.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        result = cur.fetchone()
        con.close()

        if result and check_password_hash(result[0], password):
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return """
    <h2>User Login</h2>
    <form method="POST">
        Username:
        <input name="username" required><br><br>

        Password:
        <input type="password" name="password" required><br><br>

        <button type="submit">Login</button>
    </form>
    <p>Demo login: student / student123</p>
    """


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    log_activity("/dashboard")

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT page, event_time, deviation_score, status
        FROM events
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 20
    """, (session["username"],))

    events = cur.fetchall()
    con.close()

    return render_template_string("""
        <h2>Behaviour Monitoring Dashboard</h2>

        <p>Welcome, {{ username }}</p>

        <a href="/profile">Visit Profile</a> |
        <a href="/logout">Logout</a>

        <h3>Recent Session Activities</h3>

        <table border="1" cellpadding="8">
        <tr>
            <th>Page</th>
            <th>Time</th>
            <th>Score</th>
            <th>Status</th>
        </tr>

        {% for event in events %}
        <tr>
            {% for item in event %}
            <td>{{ item }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
        </table>
    """, username=session["username"], events=events)


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    log_activity("/profile")

    return """
    <h2>User Profile</h2>
    <p>This is the profile page.</p>
    <a href="/dashboard">Back to Dashboard</a>
    """


@app.route("/logout")
def logout():
    username = session.get("username")

    if username:
        log_activity("/logout")

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)