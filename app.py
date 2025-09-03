from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Path to your Excel file
EXCEL_FILE = "Engineering Yield Tracker (1).xlsx"

def load_data():
    # Read Excel, use the 2nd row as header (index=1)
    df = pd.read_excel(EXCEL_FILE, header=1)

    # Drop completely empty rows (Excel often has them)
    df = df.dropna(how="all")

    # Melt the "wide" format into a "long" format
    melted = df.melt(
        id_vars=["Customer", "Model", "PIC", "Target Yield"],
        var_name="Day",
        value_name="FPY"
    ).dropna(subset=["FPY"])  # drop rows where FPY is empty

    # Convert to dictionary (JSON friendly)
    return melted.to_dict(orient="records")

@app.route("/data")
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)



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