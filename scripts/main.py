# Read CSV file and printing the first few rows
import pandas as pd

df = pd.read_csv("../data/BMW_sales_data_2010_2024.csv")
print(df.head())
print(df.columns)
print(df.info())

# check for duplicate rows (show them if present)
dups = df[df.duplicated(keep=False)]
if not dups.empty:
    print("Found duplicate rows (showing all duplicates):")
    print(dups)
else:
    print("No duplicate rows")

# ensure required columns exist (case-insensitive fallback for Model)
cols_map = {c.lower(): c for c in df.columns}
if "model" in cols_map:
    if cols_map["model"] != "Model":
        df = df.rename(columns={cols_map["model"]: "Model"})
else:
    raise KeyError(f"'Model' column not found. Available columns: {list(df.columns)}")

# normalize numeric columns
df["Sales_Volume"] = pd.to_numeric(df["Sales_Volume"], errors="coerce").fillna(0)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# add Yearly_Sales to every original row (sum per Model+Year)
df["Yearly_Sales"] = df.groupby(["Model", "Year"])["Sales_Volume"].transform("sum")

# create aggregated dataframe: one row per Model+Year with yearly totals
yearly = df.groupby(["Model", "Year"], as_index=False).agg({
    "Sales_Volume": "sum",    # total sales for that Model+Year
    "Price_USD": "first"      # representative price (optional)
})
yearly = yearly.rename(columns={"Sales_Volume": "Yearly_Sales"})

# ensure Price_USD is numeric before multiplication
yearly["Price_USD"] = pd.to_numeric(yearly["Price_USD"], errors="coerce").fillna(0)

# Total_Sales = Price_USD * Yearly_Sales (total revenue for that Model+Year)
yearly["Total_Sales"] = yearly["Price_USD"] * yearly["Yearly_Sales"]

# keep only the desired columns and sort for readability
organized_yearly_data = yearly[["Model", "Year", "Price_USD", "Yearly_Sales", "Total_Sales"]].sort_values(["Model", "Year"])

print(organized_yearly_data.head(20))

# visualizing data of each year sales for each model
import matplotlib.pyplot as plt

models = organized_yearly_data['Model'].unique()
for model in models:
    model_data = organized_yearly_data[organized_yearly_data['Model'] == model]
    plt.figure(figsize=(10, 6))
    plt.plot(model_data['Year'], model_data['Yearly_Sales'], marker='o')
    plt.title(f'Yearly Sales for {model}')
    plt.xlabel('Year', rotation=45)
    plt.ylabel('Yearly Sales Volume')
    plt.grid(True)
    plt.xticks(model_data['Year'])
    plt.savefig(f"../images/car_model_yearly_sales/{model}_yearly_sales.png")
    plt.show()
# Save the organized yearly data to a new CSV file
organized_yearly_data.to_csv("../data/organized_bmw_yearly_sales.csv", index=False)