import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder

from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Load cleaned dataset
df = pd.read_csv(
    "output/cleaned_ecommerce_returns.csv"
)

print("===================================")
print("MACHINE LEARNING")
print("===================================")

print(
    "Dataset Shape:",
    df.shape
)

# Target
target = "Returned"

# Features
features = [
    "Category",
    "Product_Price",
    "Quantity",
    "Region",
    "Marketing_Channel",
    "Delivery_Days",
    "Discount",
    "Payment_Method",
    "Customer_Rating"
]

X = df[features]

y = df[target]

# Categorical features
categorical_features = [
    "Category",
    "Region",
    "Marketing_Channel",
    "Payment_Method"
]

# Numerical features
numerical_features = [
    "Product_Price",
    "Quantity",
    "Delivery_Days",
    "Discount",
    "Customer_Rating"
]

# Numerical preprocessing
numeric_transformer = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="median"
        )
    )
])

# Categorical preprocessing
categorical_transformer = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="most_frequent"
        )
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])

# Combine preprocessing
preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_transformer,
        numerical_features
    ),
    (
        "categorical",
        categorical_transformer,
        categorical_features
    )
])

# Logistic Regression model
model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(
    "\nTraining rows:",
    len(X_train)
)

print(
    "Testing rows:",
    len(X_test)
)

# Train model
print(
    "\nTraining Logistic Regression..."
)

model.fit(
    X_train,
    y_train
)

print(
    "Model training completed!"
)

# Predictions
y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]

# Metrics
accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

print("\n===================================")
print("MODEL PERFORMANCE")
print("===================================")

print(
    "Accuracy :",
    round(accuracy, 4)
)

print(
    "Precision:",
    round(precision, 4)
)

print(
    "Recall   :",
    round(recall, 4)
)

print(
    "F1 Score :",
    round(f1, 4)
)

print(
    "ROC-AUC  :",
    round(roc_auc, 4)
)

print(
    "\nClassification Report:"
)

print(
    classification_report(
        y_test,
        y_pred
    )
)

print(
    "\nConfusion Matrix:"
)

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# Predict all orders
df["Return_Probability"] = model.predict_proba(
    X
)[:, 1]

# Risk levels
df["Risk_Level"] = pd.cut(
    df["Return_Probability"],
    bins=[
        -0.01,
        0.40,
        0.70,
        1.00
    ],
    labels=[
        "Low",
        "Medium",
        "High"
    ]
)

# Create folders
Path("output").mkdir(
    exist_ok=True
)

Path("model").mkdir(
    exist_ok=True
)

# Save predictions
df.to_csv(
    "output/return_predictions.csv",
    index=False
)

# High risk orders
high_risk = df[
    df["Risk_Level"] == "High"
].copy()

high_risk.to_csv(
    "output/high_risk_orders.csv",
    index=False
)

# Save model
joblib.dump(
    model,
    "model/return_prediction_model.pkl"
)

print("\n===================================")
print("PROJECT OUTPUT")
print("===================================")

print(
    "Total Orders:",
    len(df)
)

print(
    "High-Risk Orders:",
    len(high_risk)
)

print("\nFiles created:")

print(
    "1. output/return_predictions.csv"
)

print(
    "2. output/high_risk_orders.csv"
)

print(
    "3. model/return_prediction_model.pkl"
)

print(
    "\nMACHINE LEARNING COMPLETED!"
)