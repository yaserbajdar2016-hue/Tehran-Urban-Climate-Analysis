
# ============================================================
# Tehran Urban Climate Analysis
# Stage 10: Spatial Autocorrelation Analysis
# Global Moran's I and Local Moran's I (LISA)
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

# ------------------------------------------------------------
# 3. Load and validate data
# ------------------------------------------------------------

print("\nLoading spatial sample data...")

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "lon", "lat", "NDVI", "NDBI", "LST_C"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df[required_columns].copy()

df = df.apply(pd.to_numeric, errors="coerce")

if df.isna().any().any():
    raise ValueError("Missing or invalid numerical values detected.")

if not np.isfinite(df.to_numpy()).all():
    raise ValueError("Infinite values detected.")

if df.duplicated(["lon", "lat"]).any():
    raise ValueError("Duplicate coordinates detected.")

if len(df) <= K_NEIGHBORS:
    raise ValueError("Not enough observations for KNN.")

print("Number of samples:", len(df))
print("Missing values:", df.isna().sum().sum())
print("Duplicate coordinates:", df.duplicated(["lon", "lat"]).sum())

# ------------------------------------------------------------
# 4. Convert geographic coordinates to UTM
# EPSG:32639 - WGS84 / UTM zone 39N
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

df["UTM_X"] = x
df["UTM_Y"] = y

print("Coordinate projection completed.")

print("X range (meters):", x.min(), "-", x.max())
print("Y range (meters):", y.min(), "-", y.max())

# ------------------------------------------------------------
# 5. Construct spatial weights matrix
# ------------------------------------------------------------

print("\nConstructing KNN spatial weights...")

w = KNN.from_array(
    coordinates,
    k=K_NEIGHBORS
)

# Row-standardized spatial weights
w.transform = "R"

print("Spatial weights created.")
print("Number of observations:", w.n)
print("Number of neighbors per point:", K_NEIGHBORS)

# ------------------------------------------------------------
# 6. Global Moran's I
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

        np.random.seed(RANDOM_SEED)

    moran = Moran(
        values,
        w,
        transformation="R",
        permutations=PERMUTATIONS
    )     

    result = {
        "Variable": variable,
        "Samples": len(values),
        "Moran_I": moran.I,
        "Expected_I": moran.EI,
        "Z_Score": moran.z_sim,
        "P_Value": moran.p_sim,
        "Permutations": PERMUTATIONS,
        "K_Neighbors": K_NEIGHBORS
    }

    global_results.append(result)

    if moran.p_sim < SIGNIFICANCE_LEVEL:
        interpretation = "Significant spatial autocorrelation"
    else:
        interpretation = "Not statistically significant"

    print("Moran's I:", round(moran.I, 6))
    print("Expected I:", round(moran.EI, 6))
    print("Z-score:", round(moran.z_sim, 4))
    print("Pseudo p-value:", round(moran.p_sim, 4))
    print("Interpretation:", interpretation)

# Save global results
global_df = pd.DataFrame(global_results)

global_file = os.path.join(
    OUTPUT_DIR,
    "global_morans_i_results.csv"
)

global_df.to_csv(
    global_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 7. Local Moran's I (LISA)
# ------------------------------------------------------------

print("\nRunning Local Moran's I (LISA)...")

lisa_results = []

# PySAL quadrant codes:
# 1 = High-High
# 2 = Low-High
# 3 = Low-Low
# 4 = High-Low

cluster_labels = {
    1: "High-High",
    2: "Low-High",
    3: "Low-Low",
    4: "High-Low"
}

for variable in VARIABLES:

    print(f"\nCalculating LISA for {variable}...")

    values = df[variable].to_numpy()

    lisa = Moran_Local(
        values,
        w,
        transformation="R",
        permutations=PERMUTATIONS,
           )

    # Local Moran statistics
    local_i = lisa.Is
    p_values = lisa.p_sim
    quadrants = lisa.q

    # Initialize all observations as not significant
    clusters = np.full(
        len(df),
        "Not Significant",
        dtype=object
    )

    significant = p_values < SIGNIFICANCE_LEVEL

    for quadrant, label in cluster_labels.items():

        mask = significant & (quadrants == quadrant)

        clusters[mask] = label

    # Store results
    variable_results = pd.DataFrame({
        "Variable": variable,
        "Local_Morans_I": local_i,
        "P_Value": p_values,
        "Quadrant": quadrants,
        "Cluster": clusters
    })

    lisa_results.append(variable_results)

    print("\nCluster counts:")

    print(
        pd.Series(clusters)
        .value_counts()
        .to_string()
    )

# Combine LISA results
lisa_df = pd.concat(
    lisa_results,
    ignore_index=True
)

# Save LISA results
lisa_file = os.path.join(
    OUTPUT_DIR,
    "local_morans_i_results.csv"
)

lisa_df.to_csv(
    lisa_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 8. Generate LISA cluster maps
# ------------------------------------------------------------

print("\nGenerating LISA cluster maps...")

cluster_colors = {
    "High-High": "#d7191c",
    "Low-High": "#fdae61",
    "Low-Low": "#2c7bb6",
    "High-Low": "#abd9e9",
    "Not Significant": "#d9d9d9"
}

for variable in VARIABLES:

    subset = lisa_df[
        lisa_df["Variable"] == variable
    ].copy()

    fig, ax = plt.subplots(figsize=(10, 9))

    for cluster, color in cluster_colors.items():

        mask = subset["Cluster"] == cluster

        ax.scatter(
            df.loc[mask.values, "lon"],
            df.loc[mask.values, "lat"],
            c=color,
            s=9,
            label=cluster,
            alpha=0.8,
            edgecolors="none"
        )

    ax.set_title(
        f"Local Moran's I (LISA): {variable} - Tehran 2024",
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

    ax.set_aspect("equal", adjustable="datalim")

    plt.tight_layout()

    output_map = os.path.join(
        OUTPUT_DIR,
        f"LISA_{variable}.png"
    )

    plt.savefig(
        output_map,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved:", output_map)

# ------------------------------------------------------------
# 9. Save analysis summary
# ------------------------------------------------------------

summary_file = os.path.join(
    OUTPUT_DIR,
    "spatial_analysis_summary.txt"
)

with open(
    summary_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("TEHRAN URBAN CLIMATE ANALYSIS\n")
    f.write("SPATIAL AUTOCORRELATION RESULTS\n")
    f.write("=" * 50 + "\n\n")

    f.write(f"Samples: {len(df)}\n")
    f.write(f"Year: 2024\n")
    f.write(f"Spatial weights: KNN ({K_NEIGHBORS})\n")
    f.write("Coordinate system: EPSG:32639\n")
    f.write(f"Permutations: {PERMUTATIONS}\n\n")

    f.write("GLOBAL MORAN'S I RESULTS\n")
    f.write("-" * 50 + "\n")

    f.write(
        global_df.to_string(index=False)
    )

    f.write("\n\nLISA CLUSTER COUNTS\n")
    f.write("-" * 50 + "\n")

    for variable in VARIABLES:

        subset = lisa_df[
            lisa_df["Variable"] == variable
        ]

        f.write(f"\n{variable}\n")

        f.write(
            subset["Cluster"]
            .value_counts()
            .to_string()
        )

        f.write("\n")

print("\n" + "=" * 60)
print("SPATIAL AUTOCORRELATION ANALYSIS COMPLETED")
print("=" * 60)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nGenerated files:")
print("- global_morans_i_results.csv")
print("- local_morans_i_results.csv")
print("- LISA_NDVI.png")
print("- LISA_NDBI.png")
print("- LISA_LST_C.png")
print("- spatial_analysis_summary.txt")

print("\nNext step: Interpret spatial autocorrelation results.")
