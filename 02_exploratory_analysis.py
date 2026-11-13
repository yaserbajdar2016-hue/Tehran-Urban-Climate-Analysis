
# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# STAGE 02: EXPLORATORY DATA ANALYSIS
# ============================================================

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr, spearmanr, linregress

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 02: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found in data/raw")

file_path = csv_files[0]
df = pd.read_csv(file_path)

print("\nDATASET:", os.path.basename(file_path))
print("SAMPLES:", len(df))

# ------------------------------------------------------------
# 3. Select environmental variables
# ------------------------------------------------------------

variables = ["NDVI", "NDBI", "LST_C"]

data = df[variables].copy()

print("\nENVIRONMENTAL VARIABLES:")
print(data.describe())

# ------------------------------------------------------------
# 4. Pearson correlation
# ------------------------------------------------------------

pearson_matrix = data.corr(method="pearson")

print("\nPEARSON CORRELATION MATRIX:")
print(pearson_matrix.round(4))

pearson_matrix.to_csv(
    os.path.join(RESULTS_DIR, "pearson_correlation.csv")
)

# ------------------------------------------------------------
# 5. Spearman correlation
# ------------------------------------------------------------

spearman_matrix = data.corr(method="spearman")

print("\nSPEARMAN CORRELATION MATRIX:")
print(spearman_matrix.round(4))

spearman_matrix.to_csv(
    os.path.join(RESULTS_DIR, "spearman_correlation.csv")
)

# ------------------------------------------------------------
# 6. Statistical significance
# ------------------------------------------------------------

pairs = [
    ("NDVI", "LST_C"),
    ("NDBI", "LST_C"),
    ("NDVI", "NDBI")
]

print("\nPAIRWISE CORRELATION RESULTS:")

for x, y in pairs:

    pearson_r, pearson_p = pearsonr(data[x], data[y])
    spearman_r, spearman_p = spearmanr(data[x], data[y])

    print("\n", x, "vs", y)

    print("Pearson r:", round(pearson_r, 4))
    print("Pearson p-value:", pearson_p)

    print("Spearman rho:", round(spearman_r, 4))
    print("Spearman p-value:", spearman_p)

# ------------------------------------------------------------
# 7. Linear regression
# ------------------------------------------------------------

print("\nLINEAR REGRESSION RESULTS:")

for x, y in pairs:

    result = linregress(data[x], data[y])

    print("\n", y, " ~ ", x)

    print("Slope:", round(result.slope, 4))
    print("Intercept:", round(result.intercept, 4))
    print("R-squared:", round(result.rvalue ** 2, 4))
    print("P-value:", result.pvalue)

# ------------------------------------------------------------
# 8. NDVI vs LST scatter plot
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    data["NDVI"],
    data["LST_C"],
    alpha=0.35,
    s=12
)

slope, intercept = np.polyfit(
    data["NDVI"],
    data["LST_C"],
    1
)

x_line = np.linspace(
    data["NDVI"].min(),
    data["NDVI"].max(),
    100
)

plt.plot(
    x_line,
    slope * x_line + intercept,
    linewidth=2
)

plt.xlabel("NDVI")
plt.ylabel("Land Surface Temperature (°C)")
plt.title("Relationship between NDVI and LST - Tehran 2024")

plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "NDVI_vs_LST.png"),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 9. NDBI vs LST scatter plot
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    data["NDBI"],
    data["LST_C"],
    alpha=0.35,
    s=12
)

slope, intercept = np.polyfit(
    data["NDBI"],
    data["LST_C"],
    1
)

x_line = np.linspace(
    data["NDBI"].min(),
    data["NDBI"].max(),
    100
)

plt.plot(
    x_line,
    slope * x_line + intercept,
    linewidth=2
)

plt.xlabel("NDBI")
plt.ylabel("Land Surface Temperature (°C)")
plt.title("Relationship between NDBI and LST - Tehran 2024")

plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "NDBI_vs_LST.png"),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 10. Distribution analysis
# ------------------------------------------------------------

for variable in variables:

    plt.figure(figsize=(8, 5))

    plt.hist(
        data[variable],
        bins=40,
        edgecolor="black",
        alpha=0.75
    )

    plt.xlabel(variable)
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {variable} - Tehran 2024")

    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            FIGURES_DIR,
            f"{variable}_distribution.png"
        ),
        dpi=300
    )

    plt.close()

# ------------------------------------------------------------
# 11. Export cleaned analysis data
# ------------------------------------------------------------

data.to_csv(
    os.path.join(RESULTS_DIR, "environmental_variables.csv"),
    index=False
)

print("\n" + "=" * 60)
print("STAGE 02 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nRESULTS SAVED IN:", RESULTS_DIR)
print("FIGURES SAVED IN:", FIGURES_DIR)
