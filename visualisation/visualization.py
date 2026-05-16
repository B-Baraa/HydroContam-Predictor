# =========================================================
# DATA EXPLORATION VISUALIZATION (CLEAN VERSION)
# =========================================================

# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# STYLE
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8,5)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(r"data\ fused_dataset.csv")
print("✅ Dataset Loaded!")

# =========================================================
# IMPORTANT FEATURES (LIMITED & MEANINGFUL)
# =========================================================

important_features = [
    "pH",
    "Nitrate (mg/ L)",
    "Conductivity (mho/ Cm)",
    "WQI",
    "Total Coliform (MPN/ 100 mL)",
    "Turbidity (NTU)"
]

important_features = [col for col in important_features if col in df.columns]
# =========================================================
# 1. TARGET DISTRIBUTION
# =========================================================

plt.figure()
sns.countplot(x="risk_label", data=df, palette="Set2")
plt.xlabel("Risk Level (0 = Safe, 1 = High Risk)")
plt.ylabel("Number of Water Samples")
plt.title("Distribution of Water Contamination Risk")
plt.show()

# =========================================================
# 2. FEATURE DISTRIBUTIONS
# =========================================================

for col in important_features:
    plt.figure()
    sns.histplot(df[col], bins=30, kde=True)
    plt.xlabel(f"{col}")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {col}")
    plt.show()

# =========================================================
# 3. KDE BY RISK (IMPACT VISUALIZATION)
# =========================================================

for col in important_features:
    plt.figure()

    sns.kdeplot(
        data=df,
        x=col,
        hue="risk_label",
        fill=True,
        common_norm=False
    )

    plt.xlabel(col)
    plt.ylabel("Density")
    plt.title(f"Distribution of {col} by Risk Level")
    plt.legend(title="Risk", labels=["Safe", "High Risk"])
    plt.show()

# =========================================================
# 4. pH VS RISK
# =========================================================

if "pH" in df.columns:
    plt.figure()
    sns.boxplot(x="risk_label", y="pH", data=df)
    plt.xlabel("Risk Level")
    plt.ylabel("pH")
    plt.title("pH Variation Across Risk Levels")
    plt.show()

# =========================================================
# 5. NITRATE VS RISK (FIXED VIOLIN)
# =========================================================

if "Nitrate (mg/ L)" in df.columns:
    plt.figure()

    sns.violinplot(
        x="risk_label",
        y="Nitrate (mg/ L)",
        data=df,
        palette="viridis"
    )

    plt.xlabel("Risk Level")
    plt.ylabel("Nitrate Concentration (mg/L)")
    plt.title("Nitrate Distribution by Risk Level")
    plt.show()

# =========================================================
# 6. CONDUCTIVITY VS WQI
# =========================================================

if "Conductivity (mho/ Cm)" in df.columns and "WQI" in df.columns:
    plt.figure()

    sns.scatterplot(
        x="Conductivity (mho/ Cm)",
        y="WQI",
        hue="risk_label",
        data=df
    )

    plt.xlabel("Conductivity (mho/cm)")
    plt.ylabel("Water Quality Index (WQI)")
    plt.title("Conductivity vs Water Quality")
    plt.legend(title="Risk")
    plt.show()

# =========================================================
# 7. CORRELATION HEATMAP (IMPORTANT FEATURES ONLY)
# =========================================================

selected_for_corr = important_features + ["risk_label"]

plt.figure(figsize=(10,6))

corr = df[selected_for_corr].corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Between Key Water Quality Indicators")
plt.show()

# =========================================================
# 8. PAIRPLOT (CLEAN & LABELED)
# =========================================================

pairplot_features = important_features[:5] + ["risk_label"]

sample_df = df[pairplot_features].sample(min(400, len(df)))

g = sns.pairplot(
    sample_df,
    hue="risk_label",
    diag_kind="kde"
)

g.fig.suptitle(
    "Pairwise Relationships Between Key Water Features",
    y=1.02
)

plt.show()

# =========================================================
# 9. NITRATE IMPACT ON WQI
# =========================================================

if "Nitrate (mg/ L)" in df.columns and "WQI" in df.columns:
    plt.figure()

    sns.regplot(
        x="Nitrate (mg/ L)",
        y="WQI",
        data=df,
        scatter_kws={"alpha":0.5}
    )

    plt.xlabel("Nitrate (mg/L)")
    plt.ylabel("WQI")
    plt.title("Impact of Nitrate on Water Quality Index")
    plt.show()

# =========================================================
# 10. BIOLOGICAL CONTAMINATION VS RISK
# =========================================================

if "Total Coliform (MPN/ 100 mL)" in df.columns:
    plt.figure()

    sns.boxplot(
        x="risk_label",
        y="Total Coliform (MPN/ 100 mL)",
        data=df
    )

    plt.xlabel("Risk Level")
    plt.ylabel("Total Coliform (MPN/100mL)")
    plt.title("Biological Contamination Impact on Risk")
    plt.show()
#for col in important_features:
    plt.figure()

    sns.boxenplot(
        x="risk_label",
        y=col,
        data=df
    )

    plt.xlabel("Risk (0 = Safe, 1 = Risk)")
    plt.ylabel(col)

    plt.title(f"{col} — Ability to Separate Risk")

    plt.show()
#
from sklearn.preprocessing import StandardScaler

scaled_df = df.copy()

scaler = StandardScaler()
scaled_df[important_features] = scaler.fit_transform(df[important_features])

scaled_df["risk_label"] = df["risk_label"]

# Melt for plotting
melted = scaled_df.melt(
    id_vars="risk_label",
    value_vars=important_features
)

plt.figure(figsize=(10,6))

sns.boxplot(
    x="variable",
    y="value",
    hue="risk_label",
    data=melted
)

plt.xticks(rotation=45)
plt.title("Feature Impact Comparison (Normalized Scale)")
plt.ylabel("Standardized Value")

plt.show()
################
for col in important_features:
    
    df["binned"] = pd.qcut(df[col], q=10, duplicates="drop")

    risk_prob = df.groupby("binned")["risk_label"].mean()

    plt.figure()

    risk_prob.plot(marker="o")

    plt.xticks(rotation=45)
    plt.ylabel("Probability of Risk")
    plt.xlabel(col)

    plt.title(f"Risk Probability vs {col}")

    plt.show()
    ####
for col in important_features:
    
    plt.figure()

    for label in [0, 1]:
        subset = df[df["risk_label"] == label][col]

        sorted_vals = np.sort(subset)
        cdf = np.arange(len(sorted_vals)) / len(sorted_vals)

        plt.plot(sorted_vals, cdf, label=f"Risk {label}")

    plt.xscale("log")

    plt.xlabel(col)
    plt.ylabel("Cumulative Probability")
    plt.title(f"CDF of {col} by Risk Level")

    plt.legend()
    plt.show()
    ####
for col in important_features:
    
    plt.figure()

    sns.violinplot(
        x="risk_label",
        y=col,
        data=df,
        inner=None
    )

    sns.stripplot(
        x="risk_label",
        y=col,
        data=df,
        color="black",
        alpha=0.3
    )

    if df[col].max() > df[col].median() * 20:
        plt.yscale("log")

    plt.title(f"{col} Distribution with Real Data Points")

    plt.show()
####
from pandas.plotting import parallel_coordinates

sample_df = df[important_features + ["risk_label"]].sample(min(200, len(df)))

plt.figure(figsize=(10,6))

parallel_coordinates(
    sample_df,
    class_column="risk_label",
    alpha=0.3
)

plt.title("Multi-Feature Pattern of Risk vs Safe Water")

plt.xticks(rotation=45)
plt.show()
####
