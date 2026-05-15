# =========================================================
# DATA EXPLORATION VISUALIZATION
# =========================================================
# IMPORT LIBRARIES
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# STYLE
# =========================================================

sns.set_style("whitegrid")

plt.rcParams["figure.figsize"] = (8,5)

# =========================================================
# LOAD FUSED DATASET
# =========================================================

df = pd.read_csv(

    r"data\ fused_dataset.csv"

)

print("✅ Dataset Loaded!")

# =========================================================
# BASIC INFO
# =========================================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

# =========================================================
# CREATE RISK LABEL IF MISSING
# =========================================================

if "risk_label" not in df.columns:

    risk_features = [

        "Nitrate (mg/ L)",

        "Conductivity (mho/ Cm)",

        "WQI"

    ]

    risk_features = [

        col for col in risk_features

        if col in df.columns
    ]

    normalized = (

        df[risk_features] -

        df[risk_features].min()

    ) / (

        df[risk_features].max() -

        df[risk_features].min()

    )

    df["contamination_score"] = normalized.mean(axis=1)

    threshold = df[
        "contamination_score"
    ].median()

    df["risk_label"] = (

        df["contamination_score"] > threshold

    ).astype(int)

# =========================================================
# IMPORTANT FEATURES
# =========================================================

important_features = [

    "pH",

    "Nitrate (mg/ L)",

    "Conductivity (mho/ Cm)",

    "WQI",

    "Total Coliform (MPN/ 100 mL)"

]

important_features = [

    col for col in important_features

    if col in df.columns

]

# =========================================================
# 1. TARGET DISTRIBUTION
# =========================================================

plt.figure(figsize=(6,4))

sns.countplot(

    x="risk_label",

    data=df,

    palette="Set2"

)

plt.xlabel("Risk Label")

plt.ylabel("Number of Samples")

plt.title("Water Contamination Risk Distribution")

plt.show()

# =========================================================
# 2. HISTOGRAMS
# =========================================================

for col in important_features:

    plt.figure(figsize=(8,5))

    sns.histplot(

        df[col],

        bins=30,

        kde=True,

        color="skyblue"

    )

    plt.xlabel(col)

    plt.ylabel("Frequency")

    plt.title(f"Distribution of {col}")

    plt.show()

# =========================================================
# 3. PH VS RISK
# =========================================================

if "pH" in df.columns:

    plt.figure(figsize=(8,5))

    sns.boxplot(

        x="risk_label",

        y="pH",

        data=df,

        palette="coolwarm"

    )

    plt.xlabel("Risk Label")

    plt.ylabel("pH")

    plt.title("pH vs Water Contamination Risk")

    plt.show()

# =========================================================
# 4. NITRATE VS RISK
# =========================================================

if "Nitrate (mg/ L)" in df.columns:

    plt.figure(figsize=(8,5))

    sns.violinplot(

    x="Nitrate (mg/ L)",

    y="risk_label",

    data=df,

    palette="viridis",

    orient="h"

)

plt.xlabel("Nitrate Concentration (mg/L)")

plt.ylabel("Risk Level")

plt.title("Risk Level by Nitrate Concentration")

# =========================================================
# 5. CONDUCTIVITY VS RISK
# =========================================================

if "Conductivity (mho/ Cm)" in df.columns:

    plt.figure(figsize=(8,5))

    sns.scatterplot(

        x="Conductivity (mho/ Cm)",

        y="WQI",

        hue="risk_label",

        data=df,

        palette="Set1"

    )

    plt.xlabel("Conductivity")

    plt.ylabel("WQI")

    plt.title("Conductivity vs Water Quality Index")

    plt.show()

# =========================================================
# 6. KDE PLOTS
# =========================================================

for col in important_features[:4]:

    plt.figure(figsize=(8,5))

    sns.kdeplot(

        data=df,

        x=col,

        hue="risk_label",

        fill=True

    )

    plt.xlabel(col)

    plt.ylabel("Density")

    plt.title(f"{col} Density by Risk")

    plt.show()

# =========================================================
# 7. CORRELATION HEATMAP
# =========================================================

plt.figure(figsize=(14,10))

corr = df.select_dtypes(
    include=np.number
).corr()

sns.heatmap(

    corr,

    cmap="coolwarm",

    center=0

)

plt.title("Feature Correlation Heatmap")

plt.show()

# =========================================================
# 8. PAIRPLOT
# =========================================================

pairplot_features = [

    col for col in important_features

    if col in df.columns

]

pairplot_features.append(
    "risk_label"
)

sample_df = df[
    pairplot_features
].sample(
    min(400, len(df))
)

sns.pairplot(

    sample_df,

    hue="risk_label",

    palette="husl"

)

plt.show()

# =========================================================
# 9. WQI VS NITRATE
# =========================================================

if "WQI" in df.columns and "Nitrate (mg/ L)" in df.columns:

    plt.figure(figsize=(8,5))

    sns.regplot(

        x="Nitrate (mg/ L)",

        y="WQI",

        data=df,

        scatter_kws={"alpha":0.5}

    )

    plt.xlabel("Nitrate (mg/L)")

    plt.ylabel("WQI")

    plt.title("Impact of Nitrate on Water Quality")

    plt.show()

# =========================================================
# 10. COLIFORM VS RISK
# =========================================================

if "Total Coliform (MPN/ 100 mL)" in df.columns:

    plt.figure(figsize=(8,5))

    sns.boxplot(

        x="risk_label",

        y="Total Coliform (MPN/ 100 mL)",

        data=df,

        palette="magma"

    )

    plt.xlabel("Risk Label")

    plt.ylabel("Total Coliform")

    plt.title("Biological Contamination vs Risk")

    plt.show()
