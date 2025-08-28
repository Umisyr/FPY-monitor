from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def get_fpy_data():
    # Load your Excel file
    df = pd.read_excel("fpy_data.xlsx")  # replace with your file name

    # Expected columns: Customer | Model | PIC | Target Yield | 1 | 2 | 3 ... 31
    data = df.to_dict(orient="records")
    return data

@app.route("/")
def index():
    data = get_fpy_data()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
