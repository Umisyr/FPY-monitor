from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__, template_folder="templates")
CORS(app)

EXCEL_FILE = "Engineering Yield Tracker (1).xlsx"

# Helper to clean % or text
def clean_percent(x):
    if isinstance(x, str):
        x = x.strip()
        if x in ["NP", "TBC", ""]:
            return None
        if x.endswith("%"):
            try:
                return float(x[:-1])  # "95%" -> 95.0
            except ValueError:
                return None
    return x

def load_data():
    # Read Excel with 2 header rows (row 2 + 3 in Excel = index 1 + 2 in pandas)
    df = pd.read_excel(EXCEL_FILE, header=[1, 2])

    # Flatten multi-row headers
    df.columns = [
        (str(a).strip() if str(a).strip() not in ["Test Yield (FPY)", "nan", "NaN"]
         else str(b).strip())
        for a, b in df.columns
    ]

    # Drop empty rows
    df = df.dropna(how="all")

    # Forward-fill Customer names
    df["Customer"] = df["Customer"].ffill()

    # Reshape wide → long
    melted = df.melt(
        id_vars=["Customer", "Model", "PIC", "Remark", "Target Yield"],
        var_name="Day",
        value_name="FPY"
    ).dropna(subset=["FPY"])

    # Clean values
    melted["Target Yield"] = melted["Target Yield"].apply(clean_percent)
    melted["FPY"] = melted["FPY"].apply(clean_percent)

    # Convert Day to number if possible
    melted["Day"] = pd.to_numeric(melted["Day"], errors="coerce")

     # Replace NaN/NaT with None
    melted = melted.where(pd.notnull(melted), None)

    # Convert DataFrame → list of dicts
    records = melted.to_dict(orient="records")

    # 🔑 Extra pass: replace any float('nan') left inside with None
    cleaned = []
    for row in records:
        cleaned_row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        cleaned.append(cleaned_row)

    return cleaned

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/data")
def data():
    data = load_data()
    # Dump with safe JSON (None → null, no NaN)
    return app.response_class(
        response=json.dumps(data, default=str),
        status=200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(debug=True)




# from flask import Flask, jsonify
# import pandas as pd

# app = Flask(__name__)

# # Path to your Excel file
# EXCEL_FILE = "Engineering Yield Tracker (1).xlsx"

# def clean_percent(x):
#     """Convert percentage strings like '95.00%' to float, handle NP/TBC."""
#     if isinstance(x, str):
#         x = x.strip()
#         if x in ["NP", "TBC"]:
#             return None
#         if "%" in x:
#             try:
#                 return float(x.replace("%", ""))
#             except ValueError:
#                 return None
#     return x

# def load_data():
#     # Read Excel with 2 header rows
#     df = pd.read_excel(EXCEL_FILE, header=[1,2])

#     # Flatten headers
#     df.columns = [
#         str(col[0]).strip() if col[0] not in ["Test Yield (FPY)", "nan", "NaN"] else str(col[1]).strip()
#         for col in df.columns
#     ]
#     # Drop completely empty rows
#     df = df.dropna(how="all")

#     # Forward-fill Customer column
#     df["Customer"].fillna(method="ffill", inplace=True)

#     # Melt wide → long format
#     melted = df.melt(
#         id_vars=["Customer", "Model", "PIC", "Remark", "Target Yield"],
#         var_name="Day",
#         value_name="FPY"
#     ).dropna(subset=["FPY"])  # drop rows where FPY is empty

#     # Clean percentage values
#     melted["Target Yield"] = melted["Target Yield"].apply(clean_percent)
#     melted["FPY"] = melted["FPY"].apply(clean_percent)

#     return melted.to_dict(orient="records")

# @app.route("/")
# def home():
#     return "<h2>Welcome to FPY Monitoring API</h2><p>Visit <a href='/data'>/data</a> to view the dataset.</p>"

# @app.route("/data")
# def get_data():
#     data = load_data()
#     return jsonify(data)

# if __name__ == "__main__":
#     app.run(debug=True)




# import pandas as pd

# # Load file
# df = pd.read_excel("Engineering Yield Tracker (1).xlsx", sheet_name=0, header=1)   # use correct sheet index or name

# # Clean column names
# df.columns = df.columns.str.strip()

# print("Columns:", df.columns.tolist())   # <-- check what Pandas actually sees

# # Reshape from wide (days in columns) to long (one row per day)
# melted = df.melt(
#     id_vars=["Model", "PIC", "Target Yield"],   # must exactly match printed names
#     var_name="Day",
#     value_name="FPY"
# )

# # Drop NA and rows without FPY values
# melted = melted.dropna(subset=["FPY"])

# print(melted.head())