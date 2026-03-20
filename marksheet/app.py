from flask import Flask, render_template, request, redirect, flash, url_for
import pandas as pd 
import sqlite3


app = Flask(__name__)
app.secret_key = 'some_secret_key_here'

def get_db_connection():
    conn = sqlite3.connect('marksheets.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return redirect("/upload")


@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        file = request.files["excel_file"]
        df = pd.read_excel(file)
        filename = file.filename 

        marks = df["Marks"]

        stats = {
            "mean": marks.mean(),
            "median": marks.median(),
            "standard deviation" : marks.std(),
            "max": marks.max(),
            "min": marks.min()
        }

        conn = get_db_connection()
        conn.execute('INSERT INTO marksheets (name,mean,median,std,min,max) VALUES (?,?,?,?,?,?)',(filename,stats['mean'],stats['median'],stats['standard deviation'],stats['min'],stats['max']))
        conn.commit()
        conn.close()

        return render_template("stats.html",stats=stats, filename=filename)
    return render_template("upload.html")

@app.route("/marksheets")
def marksheets():
    conn = get_db_connection()
    all_marksheets = conn.execute('SELECT * FROM marksheets').fetchall()
    conn.close()
    
    if not all_marksheets:
        flash("No marksheets found! Please upload one first.")
        return redirect("/upload")
        
    return render_template("marksheets.html", marksheets = all_marksheets )

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM marksheets WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect("/marksheets")

@app.route("/stats/<int:id>")
def view_stats(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM marksheets WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if row is None:
        return "Statistics not found", 404
        
    # Format the data into the dictionary style the stats.html template expects
    stats = {
        "mean": row["mean"],
        "median": row["median"],
        "standard deviation": row["std"],
        "max": row["max"],
        "min": row["min"]
    }
    filename = row["name"]
    
    return render_template("stats.html", stats=stats, filename=filename)

if __name__ == "__main__":
    # Allowing access from any device on the network
    # host='0.0.0.0' makes the server publicly available
    app.run(host='0.0.0.0', port=5000, debug=True)