
# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# STAGE 13: FINAL MAPS AND FIGURES
# Study area: Tehran, Iran
# Study year: 2024
# Project owner: Yaser Bazhdar
# ============================================================

from pathlib import Path
import shutil
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# 1. PROJECT DIRECTORIES
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "figures"

FINAL_DIR = RESULTS_DIR / "final_figures"

FOLDERS = {
    "relationships": FINAL_DIR / "statistical_relationships",
    "autocorrelation": FINAL_DIR / "spatial_autocorrelation",
    "lisa": FINAL_DIR / "lisa_clusters",
    "regression": FINAL_DIR / "regression_models",
    "environment": FINAL_DIR / "environmental_interpretation",
}

for folder in FOLDERS.values():
    folder.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 65)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 13: FINAL MAPS AND FIGURES")
print("=" * 65)

print("\n[1] Project directories initialized.")
print("Project:", BASE_DIR)
print("Final outputs:", FINAL_DIR)


# ------------------------------------------------------------
# 2. COPY EXISTING ENVIRONMENTAL MAPS
# ------------------------------------------------------------

environmental_maps = [
    "NDVI_spatial_distribution.png",
    "NDBI_spatial_distribution.png",
    "LST_C_spatial_distribution.png",
]

print("\n[2] Selecting existing environmental maps...")

for filename in environmental_maps:

    source = FIGURES_DIR / filename
    destination = FOLDERS["environment"] / filename

    if source.exists():
        shutil.copy2(source, destination)
        print("[OK] Copied:", filename)
    else:
        print("[MISSING]", filename)


# ------------------------------------------------------------
# 3. SELECT EXISTING STATISTICAL RELATIONSHIP FIGURES
# ------------------------------------------------------------

print("\n[3] Selecting statistical relationship figures...")

relationship_file = (
    RESULTS_DIR / "regression" / "figures" /
    "regression_relationships.png"
)

if relationship_file.exists():

    destination = (
        FOLDERS["relationships"] /
        "NDVI_NDBI_LST_regression_relationships.png"
    )

    shutil.copy2(relationship_file, destination)

    print("[OK] Combined relationship figure selected.")

else:
    print("[MISSING] regression_relationships.png")


# ------------------------------------------------------------
# 4. SELECT FINAL LISA CLUSTER MAPS
# ------------------------------------------------------------

print("\n[4] Selecting BH-corrected LISA maps...")

lisa_dir = RESULTS_DIR / "spatial_autocorrelation"

lisa_maps = [
    "LISA_NDVI_BH_updated.png",
    "LISA_NDBI_BH_updated.png",
    "LISA_LST_C_BH_updated.png",
]

for filename in lisa_maps:

    source = lisa_dir / filename
    destination = FOLDERS["lisa"] / filename

    if source.exists():
        shutil.copy2(source, destination)
        print("[OK] Copied:", filename)
    else:
        print("[MISSING]", filename)


# ------------------------------------------------------------
# 5. SELECT REGRESSION DIAGNOSTICS
# ------------------------------------------------------------

print("\n[5] Selecting regression diagnostic figure...")

diagnostic_file = (
    RESULTS_DIR / "regression" / "figures" /
    "model3_residual_diagnostics.png"
)

if diagnostic_file.exists():

    destination = (
        FOLDERS["regression"] /
        "model3_residual_diagnostics.png"
    )

    shutil.copy2(diagnostic_file, destination)
    print("[OK] Regression diagnostics selected.")

else:
    print("[MISSING] model3_residual_diagnostics.png")


# ------------------------------------------------------------
# 6. LOAD SPATIAL REGRESSION RESULTS
# ------------------------------------------------------------

print("\n[6] Loading Stage 12 regression results...")

comparison_file = (
    RESULTS_DIR / "spatial_regression" /
    "model_comparison.csv"
)

moran_file = (
    RESULTS_DIR / "spatial_regression" /
    "spatial_regression_residual_moran.csv"
)

comparison = None
moran = None

if comparison_file.exists():
    comparison = pd.read_csv(comparison_file)
    print("[OK] Model comparison loaded.")
    print("Columns:", comparison.columns.tolist())
else:
    print("[MISSING]", comparison_file)

if moran_file.exists():
    moran = pd.read_csv(moran_file)
    print("[OK] Residual Moran results loaded.")
    print("Columns:", moran.columns.tolist())
else:
    print("[MISSING]", moran_file)


# ------------------------------------------------------------
# 7. PREPARE MODEL COMPARISON DATA
# ------------------------------------------------------------

def find_column(data, candidates):

    lookup = {
        str(column).strip().lower().replace(" ", "_"): column
        for column in data.columns
    }

    for candidate in candidates:
        key = candidate.lower().replace(" ", "_")
        if key in lookup:
            return lookup[key]

    return None


if comparison is not None and moran is not None:

    model_col_1 = find_column(
        comparison, ["Model", "Model_Name"]
    )

    rmse_col = find_column(
        comparison, ["RMSE", "Root_Mean_Squared_Error"]
    )

    mae_col = find_column(
        comparison, ["MAE", "Mean_Absolute_Error"]
    )

    model_col_2 = find_column(
        moran, ["Model", "Model_Name"]
    )

    moran_col = find_column(
        moran,
        ["Residual_Morans_I", "Moran_I", "Morans_I"]
    )

    required = [
        model_col_1, rmse_col, mae_col,
        model_col_2, moran_col
    ]

    if all(column is not None for column in required):

        model_data = comparison[
            [model_col_1, rmse_col, mae_col]
        ].copy()

        model_data.columns = ["Model", "RMSE", "MAE"]

        moran_data = moran[
            [model_col_2, moran_col]
        ].copy()

        moran_data.columns = ["Model", "Residual_Morans_I"]

        model_data["Model"] = (
            model_data["Model"].astype(str).str.strip()
        )

        moran_data["Model"] = (
            moran_data["Model"].astype(str).str.strip()
        )

        model_data = model_data.merge(
            moran_data,
            on="Model",
            how="inner"
        )

        model_data = model_data.replace(
            [np.inf, -np.inf], np.nan
        ).dropna()

        if not model_data.empty:

            print("\n[7] Combined model comparison:")
            print(model_data.to_string(index=False))

            # Save combined table
            model_data.to_csv(
                FOLDERS["regression"] /
                "final_model_comparison.csv",
                index=False
            )

            # ------------------------------------------------
            # 8. CREATE FINAL REGRESSION COMPARISON FIGURE
            # ------------------------------------------------

            print("\n[8] Creating regression comparison figure...")

            fig, axes = plt.subplots(
                1, 3,
                figsize=(16, 6)
            )

            metrics = [
                ("RMSE", "RMSE", "RMSE"),
                ("MAE", "MAE", "MAE"),
                (
                    "Residual_Morans_I",
                    "Residual Moran's I",
                    "Residual Moran's I"
                )
            ]

            for ax, (column, title, xlabel) in zip(
                axes, metrics
            ):

                values = model_data[column]

                bars = ax.barh(
                    model_data["Model"],
                    values
                )

                ax.set_title(title, fontsize=12)
                ax.set_xlabel(xlabel)
                ax.grid(
                    axis="x",
                    linestyle="--",
                    alpha=0.35
                )

                ax.invert_yaxis()

                for bar, value in zip(bars, values):

                    ax.text(
                        bar.get_width(),
                        bar.get_y() + bar.get_height() / 2,
                        f" {value:.3f}",
                        va="center",
                        fontsize=9
                    )

            fig.suptitle(
                "Spatial Regression Model Comparison - Tehran 2024",
                fontsize=14,
                fontweight="bold"
            )

            fig.tight_layout()

            output_figure = (
                FOLDERS["regression"] /
                "final_spatial_regression_comparison.png"
            )

            fig.savefig(
                output_figure,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close(fig)

            print("[OK] Regression comparison figure saved.")

        else:
            print("[WARNING] No matching model records.")

    else:
        print(
            "[WARNING] Required CSV columns were not identified."
        )
        print("Please inspect the column names above.")

else:
    print("[WARNING] Regression comparison not generated.")


# ------------------------------------------------------------
# 9. CREATE STAGE 13 OUTPUT INVENTORY
# ------------------------------------------------------------

print("\n[9] Creating final output inventory...")

inventory = []

for folder_name, folder_path in FOLDERS.items():

    for file in folder_path.iterdir():

        if file.is_file():

            inventory.append({
                "Category": folder_name,
                "Filename": file.name,
                "Size_KB": round(
                    file.stat().st_size / 1024, 2
                )
            })

inventory_df = pd.DataFrame(inventory)

inventory_path = FINAL_DIR / "stage13_output_inventory.csv"

inventory_df.to_csv(
    inventory_path,
    index=False
)

print("\n" + "=" * 65)
print("STAGE 13 INITIAL OUTPUTS COMPLETED")
print("=" * 65)

print("\nTotal selected/generated files:", len(inventory))

if not inventory_df.empty:
    print(inventory_df.to_string(index=False))

print("\nFinal output directory:")
print(FINAL_DIR)

print("\nOriginal project files were preserved.")
print("No Stage 1-12 analysis was rerun.")
print("\nSTAGE 13 INITIAL RUN FINISHED.")
