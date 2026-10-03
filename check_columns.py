import pandas as pd

df = pd.read_csv("dataset/ecommerce_returns.csv")

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)z