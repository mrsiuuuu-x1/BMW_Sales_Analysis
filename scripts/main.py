# Read CSV file and printing the first few rows
import pandas as pd

df = pd.read_csv("../data/BMW_sales_data_2010_2024.csv")
print(df.head())