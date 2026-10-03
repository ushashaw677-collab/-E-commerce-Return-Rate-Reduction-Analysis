import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

df = pd.read_csv(
    "output/cleaned_ecommerce_returns.csv"
)

import shutil; from pathlib import Path; p=Path("output/charts"); shutil.rmtree(p) if p.is_dir() else p.unlink() if p.exists() else None; p.mkdir(parents=True, exist_ok=True)

print("===================================")
print("EXPLORATORY DATA ANALYSIS")
print("===================================")

print("Dataset Shape:", df.shape)

# Overall return rate
return_rate = df["Returned"].mean() * 100

print(
    f"\nOverall Return Rate: {return_rate:.2f}%"
)

# Return count
print("\nReturn Count:")
print(df["Returned"].value_counts())

# Category analysis
category_analysis = df.groupby(
    "Category"
)["Returned"].agg(
    Orders="count",
    Returned="sum",
    Return_Rate="mean"
).reset_index()

category_analysis["Return_Rate"] *= 100

print("\nReturn Rate by Category:")
print(category_analysis)

# Region analysis
region_analysis = df.groupby(
    "Region"
)["Returned"].agg(
    Orders="count",
    Returned="sum",
    Return_Rate="mean"
).reset_index()

region_analysis["Return_Rate"] *= 100

print("\nReturn Rate by Region:")
print(region_analysis)

# Marketing channel analysis
channel_analysis = df.groupby(
    "Marketing_Channel"
)["Returned"].agg(
    Orders="count",
    Returned="sum",
    Return_Rate="mean"
).reset_index()

channel_analysis["Return_Rate"] *= 100

print("\nReturn Rate by Marketing Channel:")
print(channel_analysis)

# Save analysis files
category_analysis.to_csv(
    "output/category_return_analysis.csv",
    index=False
)

region_analysis.to_csv(
    "output/region_return_analysis.csv",
    index=False
)

channel_analysis.to_csv(
    "output/channel_return_analysis.csv",
    index=False
)

# Chart 1
plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Returned"
)

plt.title(
    "Returned vs Non-Returned Orders"
)

plt.xlabel(
    "Returned (0 = No, 1 = Yes)"
)

plt.ylabel(
    "Number of Orders"
)

plt.savefig(
    "output/charts/return_distribution.png",
    bbox_inches="tight"
)

plt.show()

# Chart 2
plt.figure(figsize=(9, 5))

sns.barplot(
    data=category_analysis,
    x="Category",
    y="Return_Rate"
)

plt.title(
    "Return Rate by Category"
)

plt.xlabel("Category")

plt.ylabel(
    "Return Rate (%)"
)

plt.xticks(rotation=30)

plt.savefig(
    "output/charts/category_return_rate.png",
    bbox_inches="tight"
)

plt.show()

# Chart 3
plt.figure(figsize=(8, 5))

sns.barplot(
    data=region_analysis,
    x="Region",
    y="Return_Rate"
)

plt.title(
    "Return Rate by Region"
)

plt.xlabel("Region")

plt.ylabel(
    "Return Rate (%)"
)

plt.savefig(
    "output/charts/region_return_rate.png",
    bbox_inches="tight"
)

plt.show()

# Chart 4
plt.figure(figsize=(9, 5))

sns.barplot(
    data=channel_analysis,
    x="Marketing_Channel",
    y="Return_Rate"
)

plt.title(
    "Return Rate by Marketing Channel"
)

plt.xlabel(
    "Marketing Channel"
)

plt.ylabel(
    "Return Rate (%)"
)

plt.xticks(rotation=30)

plt.savefig(
    "output/charts/channel_return_rate.png",
    bbox_inches="tight"
)

plt.show()

# Chart 5
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Returned",
    y="Delivery_Days"
)

plt.title(
    "Delivery Days vs Return Status"
)

plt.xlabel("Returned")

plt.ylabel(
    "Delivery Days"
)

plt.savefig(
    "output/charts/delivery_days_vs_return.png",
    bbox_inches="tight"
)

plt.show()

print("\n===================================")
print("EDA COMPLETED SUCCESSFULLY")
print("===================================")