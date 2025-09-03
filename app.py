from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/data")
def get_data():
    # Load Excel file (must be in same folder as this script)
    df = pd.read_excel("Engineering Yield Tracker (1).xlsx")   # columns: Date, Customer, Product, Tested, Passed
    df["FPY"] = (df["Passed"] / df["Tested"] * 100).round(2)

    # Convert to JSON and send to frontend
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)