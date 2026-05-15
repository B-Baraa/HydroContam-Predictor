# =========================================================
# 🌱 WATER CONTAMINATION RISK PREDICTION SYSTEM
# =========================================================

# =========================================================
# 1. IMPORT LIBRARIES
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================
# 3. LOAD DATASETS
# =========================================================

print("📂 Loading datasets...")

df_main = pd.read_csv(
    r"C:\Users\asus\.streamlit\data\Results_MADE.csv"
)

df_potability = pd.read_csv(
    r"C:\Users\asus\.streamlit\data\water_potability.csv"
)

df_quality = pd.read_csv(
    r"C:\Users\asus\.streamlit\data\waterQuality.csv"
)

print("✅ Datasets loaded successfully!")

# =========================================================
# 4. BASIC DATASET INFO
# =========================================================

print("\n================================================")
print("📊 DATASET SHAPES")
print("================================================")

print("Main Dataset:", df_main.shape)

print("Potability Dataset:", df_potability.shape)

print("Quality Dataset:", df_quality.shape)

# =========================================================
# 5. CLEAN EACH DATASET SEPARATELY
# =========================================================

datasets = {

    "Main": df_main,

    "Potability": df_potability,

    "Quality": df_quality

}

print("\n🧹 CLEANING DATASETS...")

for name, df in datasets.items():

    print(f"\n========== {name} ==========")

    # Remove duplicates
    before = len(df)

    df.drop_duplicates(inplace=True)

    after = len(df)

    print(f"Duplicates Removed: {before - after}")

    # Fill missing numeric values
    df.fillna(
        df.mean(numeric_only=True),
        inplace=True
    )

    print("Missing values handled!")

# =========================================================
# 6. REMOVE IMPOSSIBLE VALUES
# =========================================================

print("\n🚫 Removing impossible environmental values...")

# pH must be positive
if "pH" in df_main.columns:

    df_main = df_main[
        df_main["pH"] > 0
    ]

# Nitrate cannot be negative
if "Nitrate (mg/ L)" in df_main.columns:

    df_main = df_main[
        df_main["Nitrate (mg/ L)"] >= 0
    ]

print("✅ Impossible values removed!")

# =========================================================
# 7. OUTLIER ANALYSIS
# =========================================================

print("\n📦 OUTLIER ANALYSIS")

important_features = [

    "Nitrate (mg/ L)",

    "Conductivity (mho/ Cm)",

    "WQI",

    "Total Coliform (MPN/ 100 mL)",

    "Faecal Coliform (MPN/ 100 mL)",

    "Faecal Streptococci (MPN/ 100 mL)",

    "pH"

]

important_features = [

    col for col in important_features

    if col in df_main.columns

]

outlier_summary = []

for col in important_features:

    Q1 = df_main[col].quantile(0.25)

    Q3 = df_main[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    outliers = df_main[
        (df_main[col] < lower) |
        (df_main[col] > upper)
    ]

    percentage = (

        len(outliers) / len(df_main)

    ) * 100

    outlier_summary.append({

        "Feature": col,

        "Outlier Count": len(outliers),

        "Percentage": round(percentage, 2)

    })

# =========================================================
# 8. OUTLIER SUMMARY TABLE
# =========================================================

outlier_df = pd.DataFrame(
    outlier_summary
)

print("\n📊 OUTLIER SUMMARY")

print(outlier_df)

# =========================================================
# 9. VISUALIZE OUTLIERS
# =========================================================

for col in important_features:

    plt.figure(figsize=(8,4))

    sns.boxplot(
        x=df_main[col],
        color="skyblue"
    )

    plt.title(
        f"Outlier Detection - {col}"
    )

    plt.xlabel(col)

    plt.show()

# =========================================================
# 10. LOG TRANSFORMATION
# =========================================================

print("\n🔄 Applying Log Transformation...")

skewed_features = [

    "Nitrate (mg/ L)",

    "Total Coliform (MPN/ 100 mL)",

    "Faecal Coliform (MPN/ 100 mL)",

    "Conductivity (mho/ Cm)"

]

skewed_features = [

    col for col in skewed_features

    if col in df_main.columns

]

for col in skewed_features:

    df_main[col] = np.log1p(
        df_main[col]
    )

print("✅ Log Transformation Applied!")

# =========================================================
# 11. VISUALIZE AFTER TRANSFORMATION
# =========================================================

for col in skewed_features:

    plt.figure(figsize=(8,4))

    sns.histplot(

        df_main[col],

        bins=30,

        kde=True,

        color="orange"

    )

    plt.title(
        f"After Log Transformation - {col}"
    )

    plt.xlabel(col)

    plt.ylabel("Frequency")

    plt.show()

# =========================================================
# 12. SAVE CLEANED DATASETS
# =========================================================

print("\n💾 Saving cleaned datasets...")

df_main.to_csv(

    r"data\ cleaned_main.csv",

    index=False

)

df_potability.to_csv(

    r"data\ cleaned_potability.csv",

    index=False

)

df_quality.to_csv(

    r"data\ cleaned_quality.csv",

    index=False

)

print("✅ Cleaned datasets saved!")

# =========================================================
# 13. KEEP ONLY NUMERIC FEATURES
# =========================================================

print("\n🔢 Selecting numeric features...")

main_numeric = df_main.select_dtypes(
    include=np.number
)

pot_numeric = df_potability.select_dtypes(
    include=np.number
)

qual_numeric = df_quality.select_dtypes(
    include=np.number
)

# =========================================================
# 14. FUSE DATASETS
# =========================================================

print("\n🔗 Fusing datasets...")

min_rows = min(

    len(main_numeric),

    len(pot_numeric),

    len(qual_numeric)

)

fused_df = pd.concat([

    main_numeric.iloc[:min_rows].reset_index(drop=True),

    pot_numeric.iloc[:min_rows].reset_index(drop=True),

    qual_numeric.iloc[:min_rows].reset_index(drop=True)

], axis=1)

print("✅ Fusion completed!")

print("\nFused Dataset Shape:")

print(fused_df.shape)

# =========================================================
# 15. REMOVE DUPLICATED COLUMNS
# =========================================================

fused_df = fused_df.loc[
    :,
    ~fused_df.columns.duplicated()
]

print("✅ Duplicated columns removed!")

# =========================================================
# 16. POST-FUSION CLEANING
# =========================================================

print("\n🧹 Post-fusion cleaning...")

fused_df.fillna(

    fused_df.mean(numeric_only=True),

    inplace=True

)

print("✅ Post-fusion cleaning completed!")

# =========================================================
# REALISTIC SCIENTIFIC CONTAMINATION SCORE
# =========================================================

print("\n🌍 Creating Scientific Risk Score...")

# ---------------------------------------------------------
# WHO / EPA SAFE LIMITS
# ---------------------------------------------------------

SAFE_LIMITS = {

    "Nitrate (mg/ L)": 50,

    "Conductivity (mho/ Cm)": 500,

    "WQI": 50,

    "Total Coliform (MPN/ 100 mL)": 0,

    "Faecal Coliform (MPN/ 100 mL)": 0,

    "qual_Turbidity_avg": 5,

    "qual_Chloramines_avg": 4

}

# ---------------------------------------------------------
# WEIGHTS
# ---------------------------------------------------------

WEIGHTS = {

    "Nitrate (mg/ L)": 0.30,

    "Conductivity (mho/ Cm)": 0.10,

    "WQI": 0.15,

    "Total Coliform (MPN/ 100 mL)": 0.20,

    "Faecal Coliform (MPN/ 100 mL)": 0.15,

    "qual_Turbidity_avg": 0.05,

    "qual_Chloramines_avg": 0.05

}

# ---------------------------------------------------------
# INITIALIZE SCORE
# ---------------------------------------------------------

fused_df["contamination_score"] = 0

# ---------------------------------------------------------
# COMPUTE EXCEEDANCE RATIOS
# ---------------------------------------------------------

for feature in SAFE_LIMITS:

    if feature in fused_df.columns:

        limit = SAFE_LIMITS[feature]

        weight = WEIGHTS[feature]

        # Avoid division by zero
        if limit == 0:

            ratio = (

                fused_df[feature] > 0

            ).astype(int)

        else:

            ratio = fused_df[feature] / limit

        # Add weighted contribution
        fused_df["contamination_score"] += (

            ratio * weight

        )

# =========================================================
# PH SPECIAL CASE
# =========================================================

if "pH" in fused_df.columns:

    ph_penalty = np.where(

        (fused_df["pH"] < 6.5) |

        (fused_df["pH"] > 8.5),

        1,

        0

    )

    fused_df["contamination_score"] += (

        ph_penalty * 0.05

    )

# =========================================================
# CREATE RISK LABEL
# =========================================================

# Scientific threshold
fused_df["risk_label"] = (

    fused_df["contamination_score"] > 1

).astype(int)

print("\n✅ Scientific contamination score created!")

print("\nRisk Distribution:")

print(

    fused_df["risk_label"].value_counts()

)

# =========================================================
# 19. SAVE FUSED DATASET
# =========================================================

print("\n💾 Saving fused dataset...")

fused_df.to_csv(

    r"data\ fused_dataset.csv",

    index=False

)

print("✅ Fused dataset saved!")

# =========================================================
# 20. FINAL SUMMARY
# =========================================================

print("\n================================================")
print("🎉 PREPROCESSING & FUSION COMPLETED!")
