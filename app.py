from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn


# COVER PAGE
@app.route("/")
def cover():
    return render_template("cover.html")


# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    notebooks = conn.execute("SELECT * FROM notebooks").fetchall()
    conn.close()

    return render_template("index.html", notebooks=notebooks)


# ADD NOTEBOOK
@app.route("/add_notebook", methods=["POST"])
def add_notebook():

    name = request.form["name"]

    conn = get_db()
    conn.execute("INSERT INTO notebooks (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# OPEN NOTEBOOK
@app.route("/notebook/<int:id>")
def notebook(id):

    conn = get_db()

    notebook = conn.execute(
        "SELECT * FROM notebooks WHERE id=?",
        (id,)
    ).fetchone()

    if notebook is None:
        conn.close()
        return "Notebook not found"

    notes = conn.execute(
        "SELECT * FROM notes WHERE notebook_id=?",
        (id,)
    ).fetchall()

    conn.close()

    return render_template(
        "notebook.html",
        notebook=notebook,
        notes=notes
    )


# ADD NOTE
@app.route("/add_note/<int:notebook_id>", methods=["POST"])
def add_note(notebook_id):

    title = request.form["title"]
    content = request.form["content"]

    conn = get_db()

    conn.execute(
        "INSERT INTO notes (title, content, notebook_id) VALUES (?, ?, ?)",
        (title, content, notebook_id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("notebook", id=notebook_id))


# DELETE NOTE
@app.route("/delete_note/<int:id>/<int:notebook_id>")
def delete_note(id, notebook_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("notebook", id=notebook_id))


# CREATE DATABASE TABLES
def create_tables():
    conn = sqlite3.connect("notes.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS notebooks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        notebook_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


# RUN APP
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)