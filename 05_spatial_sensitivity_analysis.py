
# ============================================================
# Tehran Urban Climate Analysis
# Stage 10 - Spatial Sensitivity Analysis
# KNN Sensitivity: 6, 8, 10
# Permutations: 4,999
# Global Moran's I and Local Moran's I (LISA)
# FDR: Benjamini-Hochberg and Benjamini-Yekutieli
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
# 1. PROJECT PATHS
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
    "spatial_sensitivity"
)

MAP_DIR = os.path.join(
    OUTPUT_DIR,
    "maps"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MAP_DIR, exist_ok=True)

# ------------------------------------------------------------
# 2. ANALYSIS PARAMETERS
# ------------------------------------------------------------

VARIABLES = ["NDVI", "NDBI", "LST_C"]

K_VALUES = [6, 8, 10]

PERMUTATIONS = 4999

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
# 3. FDR CORRECTION
# ------------------------------------------------------------

def adjust_fdr(p_values, method="BH"):

    p_values = np.asarray(p_values, dtype=float)

    adjusted = np.full(len(p_values), np.nan)

    valid = np.isfinite(p_values)

    p = p_values[valid]

    if len(p) == 0:
        return adjusted

    if np.any((p < 0) | (p > 1)):
        raise ValueError("Invalid p-values.")

    m = len(p)

    order = np.argsort(p)

    sorted_p = p[order]

    ranks = np.arange(1, m + 1)

    if method == "BH":

        correction_factor = 1.0

    elif method == "BY":

        correction_factor = np.sum(1.0 / ranks)

    else:

        raise ValueError("Unknown FDR method.")

    adjusted_sorted = (
        sorted_p * m * correction_factor / ranks
    )

    adjusted_sorted = np.minimum.accumulate(
        adjusted_sorted[::-1]
    )[::-1]

    adjusted_sorted = np.clip(
        adjusted_sorted, 0, 1
    )

    adjusted_valid = np.empty(m)

    adjusted_valid[order] = adjusted_sorted

    adjusted[valid] = adjusted_valid

    return adjusted


# ------------------------------------------------------------
# 4. LOCAL CLUSTER CLASSIFICATION
# ------------------------------------------------------------

def classify_clusters(p_values, quadrants):

    clusters = np.full(
        len(p_values),
        "Not Significant",
        dtype=object
    )

    significant = (
        np.isfinite(p_values)
        & (p_values < SIGNIFICANCE_LEVEL)
    )

    for quadrant, label in CLUSTER_LABELS.items():

        mask = significant & (quadrants == quadrant)

        clusters[mask] = label

    return clusters


# ------------------------------------------------------------
# 5. LOAD AND VALIDATE DATA
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
        f"Missing columns: {missing_columns}"
    )

df = df[required_columns].copy()

df = df.apply(
    pd.to_numeric,
    errors="coerce"
)

if df.isna().any().any():

    raise ValueError(
        "Missing or invalid values detected."
    )

if not np.isfinite(df.to_numpy()).all():

    raise ValueError(
        "Infinite values detected."
    )

if df.duplicated(["lon", "lat"]).any():

    raise ValueError(
        "Duplicate coordinates detected."
    )

if not df["lon"].between(-180, 180).all():

    raise ValueError("Invalid longitude.")

if not df["lat"].between(-90, 90).all():

    raise ValueError("Invalid latitude.")

if len(df) <= max(K_VALUES):

    raise ValueError("Insufficient sample size.")

df.insert(
    0,
    "Sample_ID",
    np.arange(1, len(df) + 1)
)

print("Samples:", len(df))

# ------------------------------------------------------------
# 6. PROJECT COORDINATES
# ------------------------------------------------------------

print("\nProjecting coordinates...")

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

    raise ValueError(
        "Invalid projected coordinates."
    )

df["UTM_X"] = x
df["UTM_Y"] = y

print("Projection completed: EPSG:32639")

# ------------------------------------------------------------
# 7. SENSITIVITY ANALYSIS
# ------------------------------------------------------------

global_results = []

local_results = []

for k in K_VALUES:

    print("\n" + "=" * 65)

    print(f"SPATIAL WEIGHTS: KNN = {k}")

    print("=" * 65)

    # Construct a separate weights matrix for each K.

    w = KNN.from_array(
        coordinates,
        k=k
    )

    w.transform = "R"

    print("Weights created.")
    print("Observations:", w.n)
    print("Neighbors:", k)

    # --------------------------------------------------------
    # 7A. GLOBAL MORAN'S I
    # --------------------------------------------------------

    print("\nRunning Global Moran's I...")

    for variable in VARIABLES:

        print(f"\nVariable: {variable}")

        values = df[variable].to_numpy()

        if np.std(values) == 0:

            raise ValueError(
                f"Zero variance: {variable}"
            )

        # Global Moran uses NumPy random state.

        np.random.seed(RANDOM_SEED + k)

        moran = Moran(
            values,
            w,
            transformation="R",
            permutations=PERMUTATIONS
        )

        p_value = float(moran.p_sim)

        global_results.append({

            "Variable": variable,

            "K_Neighbors": k,

            "Samples": len(values),

            "Moran_I": moran.I,

            "Expected_I": moran.EI,

            "Z_Score": moran.z_sim,

            "P_Value": p_value,

            "Significant": (
                p_value < SIGNIFICANCE_LEVEL
            ),

            "Permutations": PERMUTATIONS,

            "Random_Seed": RANDOM_SEED + k

        })

        print("Moran's I:", round(moran.I, 6))
        print("Z-score:", round(moran.z_sim, 4))
        print("Pseudo p-value:", p_value)

    # --------------------------------------------------------
    # 7B. LOCAL MORAN'S I (LISA)
    # --------------------------------------------------------

    print("\nRunning Local Moran's I...")

    for variable in VARIABLES:

        print(
            f"\nCalculating LISA: {variable}, K={k}"
        )

        values = df[variable].to_numpy()

        lisa = Moran_Local(
            values,
            w,
            transformation="R",
            permutations=PERMUTATIONS,
            seed=RANDOM_SEED + k,
            n_jobs=1
        )

        local_i = lisa.Is

        p_raw = lisa.p_sim

        quadrants = lisa.q

        # FDR correction is applied separately
        # for each variable and K configuration.

        p_bh = adjust_fdr(
            p_raw,
            method="BH"
        )

        p_by = adjust_fdr(
            p_raw,
            method="BY"
        )

        clusters_raw = classify_clusters(
            p_raw,
            quadrants
        )

        clusters_bh = classify_clusters(
            p_bh,
            quadrants
        )

        clusters_by = classify_clusters(
            p_by,
            quadrants
        )

        variable_results = pd.DataFrame({

            "Sample_ID": df["Sample_ID"],

            "lon": df["lon"],

            "lat": df["lat"],

            "UTM_X": df["UTM_X"],

            "UTM_Y": df["UTM_Y"],

            "Variable": variable,

            "K_Neighbors": k,

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

        local_results.append(variable_results)

        print("\nBH cluster counts:")

        print(
            pd.Series(clusters_bh)
            .value_counts()
            .to_string()
        )

        print("\nBY significant locations:")

        print(
            np.sum(
                clusters_by != "Not Significant"
            )
        )

# ------------------------------------------------------------
# 8. SAVE GLOBAL MORAN RESULTS
# ------------------------------------------------------------

print("\nSaving global results...")

global_df = pd.DataFrame(global_results)

global_file = os.path.join(
    OUTPUT_DIR,
    "global_morans_sensitivity.csv"
)

global_df.to_csv(
    global_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 9. SAVE LOCAL MORAN RESULTS
# ------------------------------------------------------------

print("\nSaving local results...")

local_df = pd.concat(
    local_results,
    ignore_index=True
)

local_file = os.path.join(
    OUTPUT_DIR,
    "local_morans_sensitivity.csv"
)

local_df.to_csv(
    local_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 10. CLUSTER COUNTS
# ------------------------------------------------------------

print("\nCalculating cluster counts...")

count_results = []

methods = {
    "Raw": "Cluster_Raw",
    "BH": "Cluster_BH",
    "BY": "Cluster_BY"
}

for variable in VARIABLES:

    for k in K_VALUES:

        subset = local_df[
            (local_df["Variable"] == variable)
            & (local_df["K_Neighbors"] == k)
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

                count = int(
                    counts.get(cluster, 0)
                )

                count_results.append({

                    "Variable": variable,

                    "K_Neighbors": k,

                    "Method": method,

                    "Cluster": cluster,

                    "Count": count,

                    "Percentage": (
                        count / len(subset)
                    ) * 100

                })

count_df = pd.DataFrame(count_results)

count_file = os.path.join(
    OUTPUT_DIR,
    "LISA_cluster_sensitivity.csv"
)

count_df.to_csv(
    count_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 11. CLUSTER STABILITY ANALYSIS
# ------------------------------------------------------------

print("\nEvaluating cluster stability...")

stability_results = []

pairwise_comparisons = [
    (6, 8),
    (6, 10),
    (8, 10)
]

for variable in VARIABLES:

    subset = local_df[
        local_df["Variable"] == variable
    ]

    pivot = subset.pivot(
        index="Sample_ID",
        columns="K_Neighbors",
        values="Cluster_BH"
    )

    if not all(k in pivot.columns for k in K_VALUES):

        raise ValueError(
            f"Missing K configuration for {variable}"
        )

    labels_6 = pivot[6].to_numpy()
    labels_8 = pivot[8].to_numpy()
    labels_10 = pivot[10].to_numpy()

    # Stability across all three configurations.

    all_same = (
        (labels_6 == labels_8)
        & (labels_8 == labels_10)
    )

    all_significant = (
        (labels_6 != "Not Significant")
        & (labels_8 != "Not Significant")
        & (labels_10 != "Not Significant")
    )

    same_significant_cluster = (
        all_same & all_significant
    )

    stability_results.append({

        "Variable": variable,

        "Comparison": "K6_vs_K8_vs_K10",

        "Total_Samples": len(pivot),

        "Identical_Classification_Count": int(
            all_same.sum()
        ),

        "Identical_Classification_Percentage": (
            all_same.mean() * 100
        ),

        "Stable_Significant_Cluster_Count": int(
            same_significant_cluster.sum()
        ),

        "Stable_Significant_Cluster_Percentage": (
            same_significant_cluster.mean() * 100
        )

    })

    # Pairwise agreement and significant-cluster overlap.

    for k1, k2 in pairwise_comparisons:

        a = pivot[k1].to_numpy()
        b = pivot[k2].to_numpy()

        agreement = np.mean(a == b) * 100

        significant_a = (
            a != "Not Significant"
        )

        significant_b = (
            b != "Not Significant"
        )

        intersection = (
            significant_a & significant_b
        )

        union = (
            significant_a | significant_b
        )

        jaccard = (
            intersection.sum() / union.sum()
            if union.sum() > 0
            else np.nan
        )

        same_cluster = (
            intersection & (a == b)
        )

        stability_results.append({

            "Variable": variable,

            "Comparison": f"K{k1}_vs_K{k2}",

            "Total_Samples": len(pivot),

            "Identical_Classification_Count": int(
                (a == b).sum()
            ),

            "Identical_Classification_Percentage": (
                agreement
            ),

            "Stable_Significant_Cluster_Count": int(
                same_cluster.sum()
            ),

            "Stable_Significant_Cluster_Percentage": (
                same_cluster.sum() / len(pivot) * 100
            ),

            "Significant_Cluster_Jaccard": jaccard

        })

stability_df = pd.DataFrame(stability_results)

stability_file = os.path.join(
    OUTPUT_DIR,
    "LISA_cluster_stability.csv"
)

stability_df.to_csv(
    stability_file,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# 12. GENERATE BH LISA MAPS FOR EACH K
# ------------------------------------------------------------

print("\nGenerating LISA sensitivity maps...")

for variable in VARIABLES:

    for k in K_VALUES:

        subset = local_df[
            (local_df["Variable"] == variable)
            & (local_df["K_Neighbors"] == k)
        ]

        fig, ax = plt.subplots(
            figsize=(10, 9)
        )

        for cluster, color in CLUSTER_COLORS.items():

            mask = (
                subset["Cluster_BH"].values == cluster
            )

            ax.scatter(
                subset.loc[mask, "UTM_X"],
                subset.loc[mask, "UTM_Y"],
                c=color,
                s=9,
                label=cluster,
                alpha=0.8,
                edgecolors="none"
            )

        ax.set_title(
            f"LISA BH: {variable} | KNN={k} | Tehran 2024",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("UTM Easting (m)")
        ax.set_ylabel("UTM Northing (m)")

        ax.legend(
            title="Spatial Clusters",
            fontsize=8,
            loc="best"
        )

        ax.set_aspect(
            "equal",
            adjustable="datalim"
        )

        ax.grid(
            alpha=0.2,
            linestyle="--"
        )

        plt.tight_layout()

        map_file = os.path.join(
            MAP_DIR,
            f"LISA_BH_{variable}_K{k}.png"
        )

        plt.savefig(
            map_file,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Saved:", map_file)

# ------------------------------------------------------------
# 13. THREE-K CLUSTER STABILITY MAPS
# ------------------------------------------------------------

print("\nGenerating cluster stability maps...")

for variable in VARIABLES:

    subset = local_df[
        local_df["Variable"] == variable
    ]

    pivot = subset.pivot(
        index="Sample_ID",
        columns="K_Neighbors",
        values="Cluster_BH"
    )

    stable = (
        (pivot[6] == pivot[8])
        & (pivot[8] == pivot[10])
    )

    all_not_significant = (
        (pivot[6] == "Not Significant")
        & (pivot[8] == "Not Significant")
        & (pivot[10] == "Not Significant")
    )

    stable_significant = (
        stable & ~all_not_significant
    )

    map_data = df.set_index("Sample_ID").copy()

    map_data["Stability"] = "Unstable"

    map_data.loc[
        all_not_significant.index[
            all_not_significant
        ],
        "Stability"
    ] = "Stable Not Significant"

    map_data.loc[
        stable_significant.index[
            stable_significant
        ],
        "Stability"
    ] = "Stable Significant Cluster"

    stability_colors = {
        "Stable Significant Cluster": "#1a9641",
        "Stable Not Significant": "#bdbdbd",
        "Unstable": "#d7191c"
    }

    fig, ax = plt.subplots(
        figsize=(10, 9)
    )

    for category, color in stability_colors.items():

        mask = (
            map_data["Stability"] == category
        )

        ax.scatter(
            map_data.loc[mask, "UTM_X"],
            map_data.loc[mask, "UTM_Y"],
            c=color,
            s=9,
            label=category,
            alpha=0.8,
            edgecolors="none"
        )

    ax.set_title(
        f"LISA Cluster Stability: {variable} | K=6, 8, 10",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("UTM Easting (m)")
    ax.set_ylabel("UTM Northing (m)")

    ax.legend(
        fontsize=8,
        loc="best"
    )

    ax.set_aspect(
        "equal",
        adjustable="datalim"
    )

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    plt.tight_layout()

    stability_map = os.path.join(
        MAP_DIR,
        f"LISA_Stability_{variable}.png"
    )

    plt.savefig(
        stability_map,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved:", stability_map)

# ------------------------------------------------------------
# 14. GENERATE MARKDOWN SUMMARY
# ------------------------------------------------------------

print("\nGenerating sensitivity report...")

report_file = os.path.join(
    OUTPUT_DIR,
    "spatial_sensitivity_summary.md"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("# Tehran Urban Climate Analysis\n\n")

    f.write(
        "## Spatial Sensitivity Analysis\n\n"
    )

    f.write("### Study configuration\n\n")

    f.write(f"- Samples: {len(df)}\n")
    f.write("- Study year: 2024\n")
    f.write("- Variables: NDVI, NDBI, LST_C\n")
    f.write("- KNN configurations: 6, 8, 10\n")
    f.write(f"- Permutations: {PERMUTATIONS}\n")
    f.write(f"- Random seed base: {RANDOM_SEED}\n")
    f.write("- Coordinate system: EPSG:32639\n")
    f.write("- Weight transformation: Row-standardized\n")
    f.write("- FDR: BH and BY\n")
    f.write(
        f"- Significance threshold: {SIGNIFICANCE_LEVEL}\n\n"
    )

    f.write("### Global Moran's I results\n\n")

    f.write(
        global_df.to_markdown(index=False)
    )

    f.write("\n\n### LISA cluster sensitivity\n\n")

    f.write(
        count_df.to_markdown(index=False)
    )

    f.write("\n\n### Cluster stability\n\n")

    f.write(
        stability_df.to_markdown(index=False)
    )

    f.write("\n\n### Methodological considerations\n\n")

    f.write(
        "- Spatial weights were independently constructed "
        "for K=6, 8 and 10.\n"
    )

    f.write(
        "- Global and local Moran statistics were evaluated "
        "using 4,999 permutations.\n"
    )

    f.write(
        "- The approximate minimum permutation p-value "
        "is 0.0002.\n"
    )

    f.write(
        "- BH and BY corrections were applied separately "
        "for each variable and K configuration.\n"
    )

    f.write(
        "- Cluster agreement and Jaccard overlap quantify "
        "different aspects of classification stability.\n"
    )

    f.write(
        "- Agreement in the Not Significant category does "
        "not represent agreement on a significant cluster.\n"
    )

    f.write(
        "- The stability analysis evaluates sensitivity to "
        "the selected KNN configuration, not independence "
        "of spatial tests.\n"
    )

    f.write(
        "- Spatial autocorrelation does not establish "
        "causal relationships.\n"
    )

    f.write(
        "- Results remain conditional on the spatial "
        "sampling design and selected study area.\n"
    )

# ------------------------------------------------------------
# 15. FINAL OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 65)

print("SPATIAL SENSITIVITY ANALYSIS COMPLETED")

print("=" * 65)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nGenerated files:")

for filename in [
    "global_morans_sensitivity.csv",
    "local_morans_sensitivity.csv",
    "LISA_cluster_sensitivity.csv",
    "LISA_cluster_stability.csv",
    "spatial_sensitivity_summary.md"
]:

    print("-", filename)

print("\nMaps directory:")
print(MAP_DIR)

print("\nAnalysis configurations:")
print("KNN:", K_VALUES)
print("Permutations:", PERMUTATIONS)

print("\nPrevious spatial autocorrelation results were preserved.")

print("\nNext step: Review sensitivity results and maps.")
