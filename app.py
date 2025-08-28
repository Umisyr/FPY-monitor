from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# init DB
def init_db():
    conn = sqlite3.connect("fpy.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS fpy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer TEXT,
                    product TEXT,
                    fpy REAL,
                    entry_date TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer = request.form["customer"]
        product = request.form["product"]
        fpy = request.form["fpy"]
        entry_date = request.form.get("date", str(date.today()))

        conn = sqlite3.connect("fpy.db")
        c = conn.cursor()
        c.execute("INSERT INTO fpy (customer, product, fpy, entry_date) VALUES (?,?,?,?)",
                  (customer, product, fpy, entry_date))
        conn.commit()
        conn.close()

        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("fpy.db")
    c = conn.cursor()
    c.execute("SELECT entry_date, AVG(fpy) FROM fpy GROUP BY entry_date ORDER BY entry_date")
    data = c.fetchall()
    conn.close()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("dashboard.html", labels=labels, values=values)

if __name__ == "__main__":
    app.run(debug=True)