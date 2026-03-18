import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def get_db_rows(table):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        note = request.form.get("note")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if task:
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        if note:
            cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    tasks = get_db_rows('tasks')
    active_tasks = [t for t in tasks if t['status'] == 'active']
    completed_tasks = [t for t in tasks if t['status'] == 'completed']
    notes = get_db_rows('notes')

    return render_template("index.html", active_tasks=active_tasks, completed_tasks=completed_tasks, notes=notes)

@app.route("/complete_task/<int:id>", methods=["POST"])
def complete_task(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete_note/<int:id>", methods=["POST"])
def delete_note(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete_task/<int:id>", methods=["POST"])
def delete_task(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))