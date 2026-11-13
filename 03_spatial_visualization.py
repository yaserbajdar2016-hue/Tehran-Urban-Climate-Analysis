
# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# STAGE 03: SPATIAL VISUALIZATION
# ============================================================

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. Project directories
# ------------------------------------------------------------

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 03: SPATIAL VISUALIZATION")
print("=" * 60)

# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found in data/raw")

df = pd.read_csv(csv_files[0])

print("\nDATASET:", os.path.basename(csv_files[0]))
print("TOTAL SPATIAL SAMPLES:", len(df))

# ------------------------------------------------------------
# 3. Validate spatial and environmental variables
# ------------------------------------------------------------

required_columns = ["lon", "lat", "NDVI", "NDBI", "LST_C"]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df.dropna(subset=required_columns).copy()

# ------------------------------------------------------------
# 4. Define map configuration
# ------------------------------------------------------------

map_settings = {
    "NDVI": {
        "title": "Vegetation Index (NDVI)",
        "cmap": "RdYlGn",
        "label": "NDVI"
    },
    "NDBI": {
        "title": "Built-up Index (NDBI)",
        "cmap": "RdBu_r",
        "label": "NDBI"
    },
    "LST_C": {
        "title": "Land Surface Temperature",
        "cmap": "inferno",
        "label": "LST (°C)"
    }
}

# ------------------------------------------------------------
# 5. Generate spatial maps
# ------------------------------------------------------------

for variable, settings in map_settings.items():

    print(f"\nGenerating spatial map: {variable}")

    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        df["lon"],
        df["lat"],
        c=df[variable],
        cmap=settings["cmap"],
        s=12,
        alpha=0.85,
        edgecolors="none"
    )

    colorbar = plt.colorbar(scatter, ax=ax)
    colorbar.set_label(settings["label"], fontsize=11)

    ax.set_title(
        f"{settings['title']} - Tehran (2024)",
        fontsize=14,
        pad=15
    )

    ax.set_xlabel("Longitude", fontsize=11)
    ax.set_ylabel("Latitude", fontsize=11)

    ax.set_aspect("equal", adjustable="box")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    ax.set_xlim(df["lon"].min(), df["lon"].max())
    ax.set_ylim(df["lat"].min(), df["lat"].max())

    plt.tight_layout()

    output_path = os.path.join(
        FIGURES_DIR,
        f"{variable}_spatial_distribution.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("SAVED:", output_path)

# ------------------------------------------------------------
# 6. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 03 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Spatial samples:", len(df))
print("Maps generated:", len(map_settings))
print("Output directory:", FIGURES_DIR)
