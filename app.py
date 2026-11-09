from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    connection = sqlite3.connect('journal.db')
    connection.execute("""
    
    
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    connection.close()

@app.route("/")
def home():
    connection = sqlite3.connect('journal.db')
    connection.row_factory = sqlite3.Row

    entries = connection.execute(
        "SELECT * FROM entries ORDER BY id DESC"
    ).fetchall()
    connection.close()

    return render_template("index.html", entries=entries)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        connection = sqlite3.connect('journal.db')
        connection.execute(
            "INSERT INTO entries (title, content) VALUES (?, ?)",
            (title, content)
        )
        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("create.html")

@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    connection = sqlite3.connect('journal.db')
    connection.row_factory = sqlite3.Row

    entry = connection.execute(
        "SELECT * FROM entries WHERE id = ?",
        (entry_id,)
    ).fetchone()

    connection.close()

    return render_template("entry.html", entry=entry)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
