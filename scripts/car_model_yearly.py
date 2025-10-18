# visualizing data of each year sales for each model

import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_CSV = Path(__file__).resolve().parents[1] / "data" / "organized_bmw_yearly_sales.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "images" / "car_model_yearly_sales"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# load the aggregated data produced by main.py
organized_yearly_data = pd.read_csv(DATA_CSV)

# ensure Year is numeric and sorted
organized_yearly_data["Year"] = pd.to_numeric(organized_yearly_data["Year"], errors="coerce")
organized_yearly_data = organized_yearly_data.sort_values(["Model", "Year"])

# plot each model
for model in organized_yearly_data["Model"].unique():
    model_data = organized_yearly_data[organized_yearly_data["Model"] == model]
    if model_data.empty:
        continue

    plt.figure(figsize=(10, 6))
    plt.plot(model_data["Year"], model_data["Yearly_Sales"], marker="o")
    plt.title(f"Yearly Sales for {model}")
    plt.xlabel("Year")
    plt.ylabel("Yearly Sales Volume")
    plt.grid(True)
    plt.xticks(model_data["Year"].unique())
    plt.show()

    # sanitize filename and save
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", str(model))
    filepath = OUT_DIR / f"{safe_name}_yearly_sales.png"
    plt.savefig(filepath)
    plt.close()