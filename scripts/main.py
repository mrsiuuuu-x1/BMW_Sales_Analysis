# Read CSV file and printing the first few rows
import pandas as pd

df = pd.read_csv("../data/BMW_sales_data_2010_2024.csv")
# print(df.head())

# Checking whether there is any missing value in the file
# (checking all columns names)
print(df.columns)
print(df.info())
# (checking whether there are any duplicate data)
for d in df.drop_duplicates():
    if d == True:
        print(d)
    else:
        print("none duplicates")

# (checking types of car model)
car_model = df.set_index("Model").head()
print(car_model)

# (printing car models name)
models = df["Model"].dropna().unique()
for m in models:
    print(m)