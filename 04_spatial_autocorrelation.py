
# ============================================================
# Tehran Urban Climate Analysis
# Stage 10: Spatial Autocorrelation Analysis
# Reproducible Global Moran's I and Local Moran's I (LISA)
# Multiple Testing Correction: Benjamini-Hochberg and BY
# ============================================================

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyproj import Transformer
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local

warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "samples",
    "tehran_stage06_sample_2024.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "results",
    "spatial_autocorrelation"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# 2. Analysis parameters
# ------------------------------------------------------------

VARIABLES = ["NDVI", "NDBI", "LST_C"]

K_NEIGHBORS = 8
PERMUTATIONS = 999
RANDOM_SEED = 42
SIGNIFICANCE_LEVEL = 0.05

CLUSTER_LABELS = {
    1: "High-High",
    2: "Low-High",
    3: "Low-Low",
    4: "High-Low"
}

CLUSTER_COLORS = {
    "High-High": "#d7191c",
    "Low-High": "#fdae61",
    "Low-Low": "#2c7bb6",
    "High-Low": "#abd9e9",
    "Not Significant": "#d9d9d9"
}

# ------------------------------------------------------------
# 3. Multiple testing correction functions
# ------------------------------------------------------------

def adjust_fdr(p_values, method="BH"):
    """
    Calculate adjusted p-values using:
    BH = Benjamini-Hochberg
    BY = Benjamini-Yekutieli

    NaN values remain NaN.
    """

    p_values = np.asarray(p_values, dtype=float)

    adjusted = np.full(len(p_values), np.nan)

    valid = np.isfinite(p_values)

    p = p_values[valid]

    if len(p) == 0:
        return adjusted

    if np.any((p < 0) | (p > 1)):
        raise ValueError("P-values must be between 0 and 1.")

    m = len(p)

    order = np.argsort(p)
    sorted_p = p[order]

    ranks = np.arange(1, m + 1)

    if method == "BH":
        correction_factor = 1.0

    elif method == "BY":
        harmonic_number = np.sum(1.0 / ranks)
        correction_factor = harmonic_number

    else:
        raise ValueError("Method must be BH or BY.")

    adjusted_sorted = (
        sorted_p * m * correction_factor / ranks
    )

    adjusted_sorted = np.minimum.accumulate(
        adjusted_sorted[::-1]
    )[::-1]

    adjusted_sorted = np.clip(
        adjusted_sorted,
        0,
        1
    )

    adjusted_valid = np.empty(m)

    adjusted_valid[order] = adjusted_sorted

    adjusted[valid] = adjusted_valid

    return adjusted


# ------------------------------------------------------------
# 4. Cluster classification function
# ------------------------------------------------------------

def classify_clusters(p_values, quadrants, threshold):

    clusters = np.full(
        len(p_values),
        "Not Significant",
        dtype=object
    )

    significant = (
        np.isfinite(p_values)
        & (p_values < threshold)
    )

    for quadrant, label in CLUSTER_LABELS.items():

        mask = significant & (quadrants == quadrant)

        clusters[mask] = label

    return clusters


# ------------------------------------------------------------
# 5. Load and validate data
# ------------------------------------------------------------

print("\nLoading spatial sample data...")

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "lon",
    "lat",
    "NDVI",
    "NDBI",
    "LST_C"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df[required_columns].copy()

df = df.apply(
    pd.to_numeric,
    errors="coerce"
)

if df.isna().any().any():
    raise ValueError(
        "Missing or invalid numerical values detected."
    )

if not np.isfinite(df.to_numpy()).all():
    raise ValueError("Infinite values detected.")

if df.duplicated(["lon", "lat"]).any():
    raise ValueError("Duplicate coordinates detected.")

if len(df) <= K_NEIGHBORS:
    raise ValueError("Not enough observations for KNN.")

if not df["lon"].between(-180, 180).all():
    raise ValueError("Invalid longitude values.")

if not df["lat"].between(-90, 90).all():
    raise ValueError("Invalid latitude values.")

df.insert(
    0,
    "Sample_ID",
    np.arange(1, len(df) + 1)
)

print("Number of samples:", len(df))
print("Missing values:", df.isna().sum().sum())
print(
    "Duplicate coordinates:",
    df.duplicated(["lon", "lat"]).sum()
)

# ------------------------------------------------------------
# 6. Coordinate projection
# EPSG:32639 - WGS84 / UTM Zone 39N
# ------------------------------------------------------------

print("\nProjecting coordinates to UTM Zone 39N...")

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32639",
    always_xy=True
)

x, y = transformer.transform(
    df["lon"].values,
    df["lat"].values
)

coordinates = np.column_stack((x, y))

if not np.isfinite(coordinates).all():
    raise ValueError("Invalid projected coordinates.")

df["UTM_X"] = x
df["UTM_Y"] = y

print("Coordinate projection completed.")
print("X range (meters):", x.min(), "-", x.max())
print("Y range (meters):", y.min(), "-", y.max())

# ------------------------------------------------------------
# 7. Construct spatial weights
# ------------------------------------------------------------

print("\nConstructing KNN spatial weights...")

w = KNN.from_array(
    coordinates,
    k=K_NEIGHBORS
)

w.transform = "R"

print("Spatial weights created.")
print("Number of observations:", w.n)
print("Number of neighbors per point:", K_NEIGHBORS)
print("Weight transformation: Row-standardized")

# ------------------------------------------------------------
# 8. Global Moran's I
# ------------------------------------------------------------

print("\nRunning Global Moran's I...")

global_results = []

for variable in VARIABLES:

    print(f"\nAnalyzing {variable}...")

    values = df[variable].to_numpy()

    if np.std(values) == 0:
        raise ValueError(
            f"{variable} has zero variance."
        )

    # Moran in this installed ESDA version does not
    # accept a seed argument. Set NumPy seed beforehand.
    np.random.seed(RANDOM_SEED)

    moran = Moran(
        values,
        w,
        transformation="R",
        permutations=PERMUTATIONS
    )

    p_value = float(moran.p_sim)

    interpretation = (
        "Significant spatial autocorrelation"
        if p_value < SIGNIFICANCE_LEVEL
        else "Not statistically significant"
    )

    result = {
        "Variable": variable,
        "Samples": len(values),
        "Moran_I": moran.I,
        "Expected_I": moran.EI,
        "Z_Score": moran.z_sim,
        "P_Value": p_value,
        "Significance_Level": SIGNIFICANCE_LEVEL,
        "Permutations": PERMUTATIONS,
        "Random_Seed": RANDOM_SEED,
        "K_Neighbors": K_NEIGHBORS,
        "Interpretation": interpretation
    }

    global_results.append(result)

    print("Moran's I:", round(moran.I, 6))
    print("Expected I:", round(moran.EI, 6))
    print("Z-score:", round(moran.z_sim, 4))
    print("Pseudo p-value:", p_value)
    print("Interpretation:", interpretation)

global_df = pd.DataFrame(global_results)

global_file = os.path.join(
    OUTPUT_DIR,
    "global_morans_i_results_updated.csv"
)

global_df.to_csv(
    global_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:", global_file)

# ------------------------------------------------------------
# 9. Local Moran's I (LISA)
# ------------------------------------------------------------

print("\nRunning Local Moran's I (LISA)...")

lisa_results = []

for variable in VARIABLES:

    print(f"\nCalculating LISA for {variable}...")

    values = df[variable].to_numpy()

    lisa = Moran_Local(
        values,
        w,
        transformation="R",
        permutations=PERMUTATIONS,
        seed=RANDOM_SEED,
        n_jobs=1
    )

    local_i = lisa.Is
    p_raw = lisa.p_sim
    quadrants = lisa.q

    # Multiple testing corrections are performed
    # separately for each environmental variable.

    p_bh = adjust_fdr(
        p_raw,
        method="BH"
    )

    p_by = adjust_fdr(
        p_raw,
        method="BY"
    )

    # Original uncorrected classification
    clusters_raw = classify_clusters(
        p_raw,
        quadrants,
        SIGNIFICANCE_LEVEL
    )

    # Benjamini-Hochberg classification
    clusters_bh = classify_clusters(
        p_bh,
        quadrants,
        SIGNIFICANCE_LEVEL
    )

    # Benjamini-Yekutieli classification
    clusters_by = classify_clusters(
        p_by,
        quadrants,
        SIGNIFICANCE_LEVEL
    )

    variable_results = pd.DataFrame({

        "Sample_ID": df["Sample_ID"],

        "lon": df["lon"],
        "lat": df["lat"],

        "UTM_X": df["UTM_X"],
        "UTM_Y": df["UTM_Y"],

        "Variable": variable,

        "Observed_Value": values,

        "Local_Morans_I": local_i,

        "Quadrant": quadrants,

        "P_Value_Raw": p_raw,

        "P_Value_BH": p_bh,

        "P_Value_BY": p_by,

        "Cluster_Raw": clusters_raw,

        "Cluster_BH": clusters_bh,

        "Cluster_BY": clusters_by

    })

    lisa_results.append(variable_results)

    print("\nRaw cluster counts:")
    print(
        pd.Series(clusters_raw)
        .value_counts()
        .to_string()
    )

    print("\nBH cluster counts:")
    print(
        pd.Series(clusters_bh)
        .value_counts()
        .to_string()
    )

    print("\nBY cluster counts:")
    print(
        pd.Series(clusters_by)
        .value_counts()
        .to_string()
    )

# ------------------------------------------------------------
# 10. Combine and save LISA results
# ------------------------------------------------------------

lisa_df = pd.concat(
    lisa_results,
    ignore_index=True
)

lisa_file = os.path.join(
    OUTPUT_DIR,
    "local_morans_i_results_FDR.csv"
)

lisa_df.to_csv(
    lisa_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:", lisa_file)

# ------------------------------------------------------------
# 11. Compare cluster counts
# ------------------------------------------------------------

print("\nComparing cluster counts...")

count_results = []

methods = {
    "Raw": "Cluster_Raw",
    "BH": "Cluster_BH",
    "BY": "Cluster_BY"
}

for variable in VARIABLES:

    subset = lisa_df[
        lisa_df["Variable"] == variable
    ]

    for method, column in methods.items():

        counts = subset[column].value_counts()

        for cluster in [
            "High-High",
            "Low-Low",
            "High-Low",
            "Low-High",
            "Not Significant"
        ]:

            count_results.append({

                "Variable": variable,

                "Method": method,

                "Cluster": cluster,

                "Count": int(counts.get(cluster, 0)),

                "Percentage": (
                    counts.get(cluster, 0)
                    / len(subset)
                ) * 100

            })

count_df = pd.DataFrame(count_results)

count_file = os.path.join(
    OUTPUT_DIR,
    "LISA_cluster_counts_comparison.csv"
)

count_df.to_csv(
    count_file,
    index=False,
    encoding="utf-8-sig"
)

print("Saved:", count_file)

# ------------------------------------------------------------
# 12. Generate separate LISA maps
# Previous maps are preserved.
# ------------------------------------------------------------

print("\nGenerating updated LISA maps...")

map_methods = {
    "RAW": "Cluster_Raw",
    "BH": "Cluster_BH",
    "BY": "Cluster_BY"
}

for variable in VARIABLES:

    subset = lisa_df[
        lisa_df["Variable"] == variable
    ].copy()

    for method, column in map_methods.items():

        fig, ax = plt.subplots(
            figsize=(10, 9)
        )

        for cluster, color in CLUSTER_COLORS.items():

            mask = subset[column].values == cluster

            ax.scatter(
                subset.loc[mask, "lon"],
                subset.loc[mask, "lat"],
                c=color,
                s=9,
                label=cluster,
                alpha=0.8,
                edgecolors="none"
            )

        ax.set_title(
            f"LISA {method}: {variable} - Tehran 2024",
            fontsize=13,
            fontweight="bold"
        )

        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        ax.legend(
            title="Spatial Clusters",
            loc="best",
            fontsize=9
        )

        ax.grid(
            alpha=0.2,
            linestyle="--"
        )

        ax.set_aspect(
            "equal",
            adjustable="datalim"
        )

        plt.tight_layout()

        output_map = os.path.join(
            OUTPUT_DIR,
            f"LISA_{variable}_{method}_updated.png"
        )

        plt.savefig(
            output_map,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Saved:", output_map)

# ------------------------------------------------------------
# 13. Save updated analysis summary
# ------------------------------------------------------------

summary_file = os.path.join(
    OUTPUT_DIR,
    "spatial_analysis_summary_FDR.txt"
)

with open(
    summary_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("TEHRAN URBAN CLIMATE ANALYSIS\n")
    f.write("UPDATED SPATIAL AUTOCORRELATION RESULTS\n")
    f.write("=" * 65 + "\n\n")

    f.write(f"Samples: {len(df)}\n")
    f.write("Study year: 2024\n")
    f.write(f"Spatial weights: KNN ({K_NEIGHBORS})\n")
    f.write("Coordinate system: EPSG:32639\n")
    f.write(f"Permutations: {PERMUTATIONS}\n")
    f.write(f"Random seed: {RANDOM_SEED}\n")
    f.write(
        f"Significance level: {SIGNIFICANCE_LEVEL}\n\n"
    )

    f.write(
        "FDR correction: Benjamini-Hochberg (BH)\n"
    )

    f.write(
        "Sensitivity correction: Benjamini-Yekutieli (BY)\n"
    )

    f.write(
        "Correction applied separately to each variable.\n\n"
    )

    f.write("GLOBAL MORAN'S I RESULTS\n")
    f.write("-" * 65 + "\n")

    f.write(global_df.to_string(index=False))

    f.write("\n\nLISA CLUSTER COUNT COMPARISON\n")
    f.write("-" * 65 + "\n")

    for variable in VARIABLES:

        f.write(f"\n{variable}\n")

        subset = count_df[
            count_df["Variable"] == variable
        ]

        pivot = subset.pivot(
            index="Cluster",
            columns="Method",
            values="Count"
        )

        f.write(pivot.to_string())

        f.write("\n")

    f.write("\n\nMETHODOLOGICAL NOTES\n")
    f.write("-" * 65 + "\n")

    f.write(
        "1. Global Moran's I uses 999 permutation tests.\n"
    )

    f.write(
        "2. Local Moran's I uses 999 permutation tests.\n"
    )

    f.write(
        "3. A fixed random seed is used for reproducibility.\n"
    )

    f.write(
        "4. BH and BY corrections are applied separately "
        "to each variable's local tests.\n"
    )

    f.write(
        "5. Raw p-values are retained for comparison.\n"
    )

    f.write(
        "6. Permutation p-values have finite resolution. "
        "With 999 permutations, the minimum attainable "
        "pseudo p-value is approximately 0.001.\n"
    )

    f.write(
        "7. Results depend on the KNN spatial weights "
        "and the spatial sampling design.\n"
    )

    f.write(
        "8. Statistical significance does not establish "
        "causality.\n"
    )

print("\nSaved:", summary_file)

# ------------------------------------------------------------
# 14. Final report
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("UPDATED SPATIAL AUTOCORRELATION ANALYSIS COMPLETED")
print("=" * 65)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nGenerated files:")

print("- global_morans_i_results_updated.csv")
print("- local_morans_i_results_FDR.csv")
print("- LISA_cluster_counts_comparison.csv")
print("- spatial_analysis_summary_FDR.txt")

print("\nMaps generated for:")

for variable in VARIABLES:

    print(
        f"- {variable}: RAW, BH and BY maps"
    )

print("\nPrevious results have not been intentionally overwritten.")

print("\nNext step: Evaluate FDR results and spatial sensitivity.")
