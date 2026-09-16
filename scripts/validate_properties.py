#Validates the property dataset for missing values, duplicate IDs, invalid prices, and property status.

import pandas as pd

FILE_PATH = "data/properties.csv"

df = pd.read_csv(FILE_PATH)

print("=== PROPERTY DATASET VALIDATION ===")
print(f"Total properties: {len(df)}")
print(f"Columns: {list(df.columns)}")

print("\n=== Missing Values ===")
print(df.isnull().sum())

print("\n=== Duplicate Property IDs ===")
print(f"Duplicates: {df['property_id'].duplicated().sum()}")

print("\n=== Invalid Prices ===")
print(f"Invalid prices: {(df['price_lakh'] <= 0).sum()}")

print("\n=== Property Status ===")
print(df["status"].value_counts())

print("\n=== Validation Complete ===")