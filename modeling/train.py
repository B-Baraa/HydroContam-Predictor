# =========================================================
# IMPORT LIBRARIES
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pickle

# LOAD FUSED DATASET

df = pd.read_csv(

    r"data\ fused_dataset.csv"

)
# =========================================================
# DEFINE FEATURES & TARGET
# =========================================================

excluded_columns = [

    "risk_label",

    "contamination_score"

]

features = [

    col for col in df.columns

    if col not in excluded_columns

]

# Keep numeric features only
features = [

    col for col in features

    if pd.api.types.is_numeric_dtype(df[col])

]

X = df[features]

y = df["risk_label"]
# =========================================================
# 16. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
# =========================================================
# MODELS
# =========================================================

models = {

    "Random Forest": RandomForestClassifier(),

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Decision Tree": DecisionTreeClassifier()

}

results = {}
# =========================================================
# 18. MODEL TRAINING & EVALUATION
# =========================================================

print("\n🚀 Training Models...")

for name, model in models.items():

    print(f"\n================ {name} ================")

    # Train
    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    results[name] = accuracy

    # Train vs Test accuracy
    train_acc = model.score(
        X_train,
        y_train
    )

    test_acc = model.score(
        X_test,
        y_test
    )

    print("Train Accuracy:", train_acc)

    print("Test Accuracy:", test_acc)

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )
# =========================================================
# 19. MODEL COMPARISON
# =========================================================

print("\n📊 Model Comparison...")

plt.figure(figsize=(8,5))

plt.bar(
    results.keys(),
    results.values()
)

plt.title("Model Accuracy Comparison")

plt.ylabel("Accuracy")

plt.show()
# =========================================================
# 20. SELECT BEST MODEL
# =========================================================

best_model_name = max(
    results,
    key=results.get
)

best_model = models[best_model_name]

print("\n🏆 BEST MODEL:")
print(best_model_name)
# =========================================================
# 21. CONFUSION MATRICES
# =========================================================

for name, model in models.items():

    predictions = model.predict(X_test)

    cm = confusion_matrix(
        y_test,
        predictions
    )

    plt.figure(figsize=(5,4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title(f"{name} Confusion Matrix")

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.show()

# 22. ROC CURVES
# =========================================================

print("\n📈 ROC Curves...")

plt.figure(figsize=(8,6))

for name, model in models.items():

    probs = model.predict_proba(X_test)[:,1]

    fpr, tpr, _ = roc_curve(
        y_test,
        probs
    )

    roc_auc = auc(
        fpr,
        tpr
    )

    plt.plot(
        fpr,
        tpr,
        label=f"{name} (AUC={roc_auc:.2f})"
    )

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve Comparison")

plt.legend()

plt.show()

# =========================================================
# 23. FEATURE IMPORTANCE
# =========================================================

if hasattr(best_model, "feature_importances_"):

    print("\n📊 Feature Importance...")

    importance_df = pd.DataFrame({

        "Feature": X.columns,

        "Importance": best_model.feature_importances_

    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=True
    )

    plt.figure(figsize=(10,8))

    plt.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    plt.title("Feature Importance")

    plt.xlabel("Importance Score")

    plt.show()
# =========================================================
# 25. SAVE MODEL
# =========================================================

print("\n💾 Saving Model...")

with open("best_model.pkl", "wb") as f:

    pickle.dump(best_model, f)

with open("features.pkl", "wb") as f:

    pickle.dump(features, f)

print("✅ Model Saved Successfully!")