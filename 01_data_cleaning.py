import pandas as pd
from pathlib import Path

input_file = "dataset/ecommerce_returns.csv"
output_file = "output/cleaned_ecommerce_returns.csv"

Path("output").mkdir(exist_ok=True)

df = pd.read_csv(input_file)

print("===================================")
print("DATA CLEANING")
print("===================================")

print("Original Shape:", df.shape)

print("\nOriginal Columns:")
print(df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Convert numerical columns
numeric_columns = [
    "Product_Price",
    "Quantity",
    "Delivery_Days",
    "Discount",
    "Customer_Rating",
    "Returned"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Fill missing numerical values
for column in numeric_columns:
    df[column] = df[column].fillna(
        df[column].median()
    )

# Categorical columns
categorical_columns = [
    "Category",
    "Region",
    "Marketing_Channel",
    "Payment_Method"
]

# Fill missing categorical values
for column in categorical_columns:
    df[column] = df[column].fillna(
        df[column].mode()[0]
    )

# Convert target column to integer
df["Returned"] = df["Returned"].astype(int)

# Create output folder
Path("output").mkdir(
    parents=True,
    exist_ok=True
)

# Save cleaned dataset
df.to_csv(
    output_file,
    index=False
)

print("\n===================================")
print("CLEANING COMPLETED")
print("===================================")

print("Cleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nSaved File:")
print(output_file)