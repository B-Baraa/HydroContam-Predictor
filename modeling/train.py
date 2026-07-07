# =========================================================
# IMPORT LIBRARIES
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
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
from imblearn.over_sampling import SMOTE
import pickle

# =========================================================
# LOAD FUSED DATASET
# =========================================================

df = pd.read_csv(r"data\ fused_dataset.csv")

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

features = [
    col for col in features
    if pd.api.types.is_numeric_dtype(df[col])
]

X = df[features]
y = df["risk_label"]

# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y          # FIX: preserve class ratio in both splits
)

# =========================================================
# HANDLE CLASS IMBALANCE WITH SMOTE
# =========================================================

print("⚖️ Applying SMOTE to balance training data...")

sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train, y_train)

print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
print(f"After  SMOTE: {pd.Series(y_train_bal).value_counts().to_dict()}")

# =========================================================
# MODELS — with overfitting protection
# =========================================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=4,            # FIX: prevent overly deep trees
        min_samples_leaf=5,     # FIX: avoid splits on tiny groups
        class_weight="balanced",
        random_state=42
    ),

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=4,            # FIX: prevent perfect memorization
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42
    )
}

results = {}

# =========================================================
# MODEL TRAINING & EVALUATION
# =========================================================

print("\n🚀 Training Models...")

for name, model in models.items():

    print(f"\n================ {name} ================")

    # Train on SMOTE-balanced data
    model.fit(X_train_bal, y_train_bal)

    # Predictions
    predictions = model.predict(X_test)

    # FIX: use F1 for imbalanced data, not just accuracy
    accuracy   = accuracy_score(y_test, predictions)
    report     = classification_report(y_test, predictions, output_dict=True)
    f1_class1  = report["1"]["f1-score"]
    recall_class1 = report["1"]["recall"]

    results[name] = {
        "accuracy":  accuracy,
        "f1_risk":   f1_class1,
        "recall_risk": recall_class1,
        "model":     model
    }

    # Overfitting check: train vs test accuracy
    train_acc = model.score(X_train_bal, y_train_bal)
    test_acc  = model.score(X_test, y_test)

    print(f"Train Accuracy : {train_acc:.4f}")
    print(f"Test  Accuracy : {test_acc:.4f}")
    print(f"Gap (overfit?) : {train_acc - test_acc:.4f}  {'⚠️ Check this' if train_acc - test_acc > 0.1 else '✅ OK'}")
    print(f"\nF1  (class 1)  : {f1_class1:.4f}")
    print(f"Recall (class 1): {recall_class1:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))

# =========================================================
# STRATIFIED CROSS-VALIDATION (overfitting check)
# =========================================================

print("\n🔁 Cross-Validation (Recall on contaminated class)...")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, info in results.items():

    scores = cross_val_score(
        info["model"],
        X, y,
        cv=cv,
        scoring="recall"
    )

    print(f"\n{name}")
    print(f"  Recall per fold : {np.round(scores, 3)}")
    print(f"  Mean  : {scores.mean():.3f}")
    print(f"  Std   : {scores.std():.3f}  {'⚠️ Unstable' if scores.std() > 0.15 else '✅ Stable'}")

# =========================================================
# MODEL COMPARISON PLOT
# =========================================================

print("\n📊 Model Comparison...")

names      = list(results.keys())
accuracies = [results[n]["accuracy"]    for n in names]
f1_scores  = [results[n]["f1_risk"]     for n in names]
recalls    = [results[n]["recall_risk"] for n in names]

x = np.arange(len(names))
width = 0.25

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - width, accuracies, width, label="Accuracy",       color="#4CAF93")
ax.bar(x,         f1_scores,  width, label="F1 (class 1)",   color="#42A5F5")
ax.bar(x + width, recalls,    width, label="Recall (class 1)",color="#E05C5C")

ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel("Score")
ax.set_title("Model Comparison — Accuracy vs F1 vs Recall (contamination class)")
ax.legend()
ax.set_ylim(0, 1.1)
plt.tight_layout()
plt.show()

# =========================================================
# SELECT BEST MODEL — by F1 on class 1, not accuracy
# =========================================================

best_model_name = max(
    results,
    key=lambda n: results[n]["f1_risk"]   # FIX: was using accuracy
)

best_model = results[best_model_name]["model"]

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   F1 (class 1) : {results[best_model_name]['f1_risk']:.4f}")
print(f"   Recall       : {results[best_model_name]['recall_risk']:.4f}")

# =========================================================
# CONFUSION MATRICES
# =========================================================

for name, info in results.items():

    predictions = info["model"].predict(X_test)
    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

# =========================================================
# ROC CURVES
# =========================================================

print("\n📈 ROC Curves...")

plt.figure(figsize=(8, 6))

for name, info in results.items():

    probs   = info["model"].predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label=f"{name} (AUC={roc_auc:.2f})")

plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.tight_layout()
plt.show()

# =========================================================
# FEATURE IMPORTANCE
# =========================================================

if hasattr(best_model, "feature_importances_"):

    print("\n📊 Feature Importance...")

    importance_df = pd.DataFrame({
        "Feature":    X.columns,
        "Importance": best_model.feature_importances_
    }).sort_values(by="Importance", ascending=True)

    plt.figure(figsize=(10, 8))
    plt.barh(importance_df["Feature"], importance_df["Importance"], color="#42A5F5")
    plt.title("Feature Importance — Best Model")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.show()

# =========================================================
# SAVE MODEL
# =========================================================

print("\n💾 Saving Model...")

with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("features.pkl", "wb") as f:
    pickle.dump(features, f)

print("✅ Model Saved Successfully!")