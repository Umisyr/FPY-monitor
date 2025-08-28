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

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    customer_filter = request.args.get("customer")
    product_filter = request.args.get("product")

    conn = sqlite3.connect("fpy.db")
    c = conn.cursor()

    query = "SELECT entry_date, AVG(fpy) FROM fpy WHERE 1=1"
    params = []

    if customer_filter:
        query += " AND customer=?"
        params.append(customer_filter)

    if product_filter:
        query += " AND product=?"
        params.append(product_filter)

    query += " GROUP BY entry_date ORDER BY entry_date"
    c.execute(query, params)
    data = c.fetchall()

    # Get distinct customers & products for dropdown
    c.execute("SELECT DISTINCT customer FROM fpy")
    customers = [row[0] for row in c.fetchall()]

    c.execute("SELECT DISTINCT product FROM fpy")
    products = [row[0] for row in c.fetchall()]

    conn.close()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("dashboard.html",
                           labels=labels,
                           values=values,
                           customers=customers,
                           products=products,
                           customer_filter=customer_filter,
                           product_filter=product_filter)

if __name__ == "__main__":
    app.run(debug=True)
