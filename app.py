from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/data")
def get_data():
    # Load your Excel file
    df = pd.read_excel("Engineering Yield Tracker (1).xlsx", sheet_name=0, header=1)  # Row 2 as header

    # Select relevant parts
    base_cols = ["Model", "PIC", "Target Yield"]
    date_cols = [c for c in df.columns if isinstance(c, (int, float)) or str(c).isdigit()]

    # Melt (reshape wide → long)
    long_df = df.melt(
        id_vars=base_cols,
        value_vars=date_cols,
        var_name="Day",
        value_name="FPY"
    )

    # Clean data
    long_df = long_df.dropna(subset=["FPY"])          # drop empty cells
    long_df = long_df[~long_df["FPY"].isin(["NP","TBC"])]  # remove NP/TBC
    long_df["FPY"] = long_df["FPY"].astype(str).str.replace("%","").astype(float)

    # Example: add full date (assuming August 2025)
    long_df["Date"] = pd.to_datetime("2025-08-" + long_df["Day"].astype(str), errors="coerce")

    # Convert to JSON
    return jsonify(long_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)


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