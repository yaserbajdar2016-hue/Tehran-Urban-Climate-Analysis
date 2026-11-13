# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# STAGE 13A: SPATIAL AUTOCORRELATION FINAL FIGURES
# Study area: Tehran, Iran
# Study year: 2024
# ============================================================
from pathlib import Path
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
warnings.filterwarnings("ignore")
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
OUTPUT_DIR = RESULTS_DIR / "final_figures" / "spatial_autocorrelation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
GLOBAL_FILE = (
    RESULTS_DIR / "spatial_autocorrelation" /
    "global_morans_i_results_updated.csv"
)
RESIDUAL_FILE = (
    RESULTS_DIR / "spatial_regression" /
    "spatial_regression_residual_moran.csv"
)
def save_new_figure(fig, filename):
    """Save a figure without overwriting an existing file."""
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        print("[SKIPPED - EXISTS]", output_path.name)
        plt.close(fig)
        return
    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )
    plt.close(fig)
    print("[OK] Saved:", output_path.name)
def save_new_csv(data, filename):
    """Save a CSV without overwriting an existing file."""
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        print("[SKIPPED - EXISTS]", output_path.name)
        return
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("[OK] Saved:", output_path.name)
def find_column(data, candidates):
    lookup = {
        str(column).strip().lower().replace(" ", "_"): column
        for column in data.columns
    }
    for candidate in candidates:
        key = candidate.strip().lower().replace(" ", "_")
        if key in lookup:
            return lookup[key]
    return None
print("\n" + "=" * 65)
print("STAGE 13A: SPATIAL AUTOCORRELATION FINAL FIGURES")
print("=" * 65)
# ------------------------------------------------------------
# 1. CHECK AND LOAD SOURCE DATA
# ------------------------------------------------------------
if not GLOBAL_FILE.exists():
    raise FileNotFoundError(
        f"Global Moran file not found: {GLOBAL_FILE}"
    )
if not RESIDUAL_FILE.exists():
    raise FileNotFoundError(
        f"Residual Moran file not found: {RESIDUAL_FILE}"
    )
global_data = pd.read_csv(GLOBAL_FILE)
residual_data = pd.read_csv(RESIDUAL_FILE)
print("\n[1] Source datasets loaded.")
print("Global Moran columns:", global_data.columns.tolist())
print("Residual Moran columns:", residual_data.columns.tolist())
# ------------------------------------------------------------
# 2. VALIDATE GLOBAL MORAN DATA
# ------------------------------------------------------------
global_variable = find_column(
    global_data, ["Variable"]
)
global_moran = find_column(
    global_data, ["Moran_I", "Morans_I"]
)
global_p = find_column(
    global_data, ["P_Value", "P_Value_Sim"]
)
if any(x is None for x in [global_variable, global_moran, global_p]):
    raise ValueError(
        "Required columns are missing from the Global Moran CSV."
    )
global_plot = global_data[
    [global_variable, global_moran, global_p]
].copy()
global_plot.columns = ["Variable", "Moran_I", "P_Value"]
global_plot["Variable"] = (
    global_plot["Variable"].astype(str).str.strip()
)
global_plot["Moran_I"] = pd.to_numeric(
    global_plot["Moran_I"], errors="coerce"
)
global_plot["P_Value"] = pd.to_numeric(
    global_plot["P_Value"], errors="coerce"
)
global_plot = global_plot.dropna(
    subset=["Variable", "Moran_I", "P_Value"]
)
if global_plot.empty:
    raise ValueError("No valid Global Moran records were found.")
# ------------------------------------------------------------
# 3. GLOBAL MORAN'S I COMPARISON FIGURE
# ------------------------------------------------------------
print("\n[2] Creating Global Moran's I comparison...")
global_order = ["NDVI", "NDBI", "LST_C"]
global_plot["sort_order"] = global_plot["Variable"].apply(
    lambda x: global_order.index(x) if x in global_order else 99
)
global_plot = global_plot.sort_values("sort_order")
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(
    global_plot["Variable"],
    global_plot["Moran_I"],
    width=0.58
)
ax.axhline(
    0,
    linewidth=0.9,
    linestyle="--",
    alpha=0.7
)
for bar, (_, row) in zip(bars, global_plot.iterrows()):
    value = row["Moran_I"]
    p_value = row["P_Value"]
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.018,
        f"I = {value:.3f}\np = {p_value:.3f}",
        ha="center",
        va="bottom",
        fontsize=9
    )
ax.set_title(
    "Global Spatial Autocorrelation of Environmental Variables\n"
    "Tehran, 2024 | KNN = 8",
    fontsize=12,
    fontweight="bold",
    pad=14
)
ax.set_xlabel("Environmental variable")
ax.set_ylabel("Global Moran's I")
ax.set_ylim(
    0,
    max(0.85, global_plot["Moran_I"].max() + 0.15)
)
ax.grid(
    axis="y",
    linestyle=":",
    alpha=0.35
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
save_new_figure(
    fig,
    "global_morans_i_comparison.png"
)
# ------------------------------------------------------------
# 4. VALIDATE RESIDUAL MORAN DATA
# ------------------------------------------------------------
residual_model = find_column(
    residual_data, ["Model", "Model_Name"]
)
residual_moran = find_column(
    residual_data,
    ["Moran_I", "Residual_Morans_I", "Morans_I"]
)
residual_p = find_column(
    residual_data, ["P_Value", "P_Value_Sim"]
)
if any(x is None for x in [
    residual_model, residual_moran, residual_p
]):
    raise ValueError(
        "Required columns are missing from the residual Moran CSV."
    )
residual_plot = residual_data[
    [residual_model, residual_moran, residual_p]
].copy()
residual_plot.columns = ["Model", "Moran_I", "P_Value"]
residual_plot["Model"] = (
    residual_plot["Model"].astype(str).str.strip()
)
residual_plot["Moran_I"] = pd.to_numeric(
    residual_plot["Moran_I"], errors="coerce"
)
residual_plot["P_Value"] = pd.to_numeric(
    residual_plot["P_Value"], errors="coerce"
)
residual_plot = residual_plot.dropna(
    subset=["Model", "Moran_I", "P_Value"]
)
if residual_plot.empty:
    raise ValueError("No valid residual Moran records were found.")
# ------------------------------------------------------------
# 5. RESIDUAL SPATIAL AUTOCORRELATION FIGURE
# ------------------------------------------------------------
print("\n[3] Creating residual spatial autocorrelation comparison...")
model_order = ["OLS", "GM_Lag", "GM_Error_Het"]
residual_plot["sort_order"] = residual_plot["Model"].apply(
    lambda x: model_order.index(x) if x in model_order else 99
)
residual_plot = residual_plot.sort_values("sort_order")
fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(
    residual_plot["Model"],
    residual_plot["Moran_I"],
    width=0.58
)
ax.axhline(
    0,
    linewidth=0.9,
    linestyle="--",
    alpha=0.7
)
for bar, (_, row) in zip(bars, residual_plot.iterrows()):
    value = row["Moran_I"]
    p_value = row["P_Value"]
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.018,
        f"I = {value:.3f}\np = {p_value:.3f}",
        ha="center",
        va="bottom",
        fontsize=9
    )
ax.set_title(
    "Residual Spatial Autocorrelation by Regression Model\n"
    "Tehran, 2024 | KNN = 8",
    fontsize=12,
    fontweight="bold",
    pad=14
)
ax.set_xlabel("Regression model")
ax.set_ylabel("Residual Moran's I")
ax.set_ylim(
    min(0, residual_plot["Moran_I"].min() - 0.05),
    max(0.85, residual_plot["Moran_I"].max() + 0.15)
)
ax.grid(
    axis="y",
    linestyle=":",
    alpha=0.35
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
save_new_figure(
    fig,
    "residual_spatial_autocorrelation_comparison.png"
)
# ------------------------------------------------------------
# 6. COMBINED ANALYTICAL SUMMARY
# ------------------------------------------------------------
print("\n[4] Preparing combined analytical summary...")
global_summary = global_plot.copy()
global_summary.insert(
    0, "Analysis_Type", "Global_Morans_I"
)
global_summary = global_summary.rename(
    columns={"Variable": "Indicator_or_Model"}
)
residual_summary = residual_plot.copy()
residual_summary.insert(
    0, "Analysis_Type", "Residual_Morans_I"
)
residual_summary = residual_summary.rename(
    columns={"Model": "Indicator_or_Model"}
)
summary = pd.concat(
    [global_summary, residual_summary],
    ignore_index=True
)
summary = summary[
    ["Analysis_Type", "Indicator_or_Model", "Moran_I", "P_Value"]
]
save_new_csv(
    summary,
    "spatial_autocorrelation_final_summary.csv"
)
# ------------------------------------------------------------
# 7. SCIENTIFIC INTERPRETATION REPORT
# ------------------------------------------------------------
global_values = {
    row["Variable"]: row
    for _, row in global_plot.iterrows()
}
residual_values = {
    row["Model"]: row
    for _, row in residual_plot.iterrows()
}
required_global = ["NDVI", "NDBI", "LST_C"]
required_models = ["OLS", "GM_Lag", "GM_Error_Het"]
missing_global = [
    name for name in required_global
    if name not in global_values
]
missing_models = [
    name for name in required_models
    if name not in residual_values
]
if missing_global or missing_models:
    print("\n[WARNING] Some expected records are missing.")
    print("Missing global variables:", missing_global)
    print("Missing regression models:", missing_models)
else:
    ndvi = global_values["NDVI"]["Moran_I"]
    ndbi = global_values["NDBI"]["Moran_I"]
    lst = global_values["LST_C"]["Moran_I"]
    ols = residual_values["OLS"]["Moran_I"]
    lag = residual_values["GM_Lag"]["Moran_I"]
    error = residual_values["GM_Error_Het"]["Moran_I"]
    lag_p = residual_values["GM_Lag"]["P_Value"]
    reduction = (
        (ols - lag) / abs(ols) * 100
        if ols != 0 else np.nan
    )
    report = f"""# Spatial Autocorrelation Analysis
## Tehran Urban Climate Analysis – Stage 13
Study area: Tehran, Iran
Study year: 2024
### 1. Global Moran's I
| Variable | Moran's I | P-value |
|---|---:|---:|
| NDVI | {ndvi:.4f} | {global_values['NDVI']['P_Value']:.4f} |
| NDBI | {ndbi:.4f} | {global_values['NDBI']['P_Value']:.4f} |
| LST | {lst:.4f} | {global_values['LST_C']['P_Value']:.4f} |
All three indicators show positive spatial autocorrelation.
LST has the strongest spatial clustering, followed by NDVI and NDBI.
These results indicate that similar environmental values tend to occur near one another.
Global Moran's I describes overall spatial association; it does not identify the geographic location of individual clusters.
Local cluster locations are examined using LISA.
### 2. Residual Spatial Autocorrelation
| Model | Residual Moran's I | P-value |
|---|---:|---:|
| OLS | {ols:.4f} | {residual_values['OLS']['P_Value']:.4f} |
| GM_Lag | {lag:.4f} | {lag_p:.4f} |
| GM_Error_Het | {error:.4f} | {residual_values['GM_Error_Het']['P_Value']:.4f} |
GM_Lag reduces residual Moran's I by approximately {reduction:.1f}% relative to OLS.
However, its residual Moran's I remains statistically significant (p = {lag_p:.4f}).
Therefore, the remaining spatial autocorrelation has been substantially reduced but not eliminated.
### 3. Interpretation and Limitations
The stronger global clustering of LST suggests that land surface temperature has a more pronounced spatial structure than NDVI and NDBI in the study area.
Residual diagnostics indicate that spatial dependence remains important when evaluating regression model performance.
The Pseudo-R-squared of GM_Lag should not be directly compared with the conventional OLS R-squared.
Global Moran's I and LISA provide complementary information: the former measures overall spatial autocorrelation, while the latter identifies local clusters and spatial outliers.
### 4. Source Data and Configuration
- Global Moran source: `results/spatial_autocorrelation/global_morans_i_results_updated.csv`
- Residual Moran source: `results/spatial_regression/spatial_regression_residual_moran.csv`
- Global Moran neighborhood: KNN = 8
- Global Moran permutations: 999
- Global Moran random seed: 42
- Sample size for the principal spatial analysis: 5,000
P-values are reported as stored in the source datasets.
"""
    report_path = OUTPUT_DIR / "spatial_autocorrelation_analysis.md"
    if report_path.exists():
        print("[SKIPPED - EXISTS]", report_path.name)
    else:
        report_path.write_text(report, encoding="utf-8")
        print("[OK] Saved:", report_path.name)
# ------------------------------------------------------------
# 8. FINAL STATUS
# ------------------------------------------------------------
print("\n" + "=" * 65)
print("STAGE 13A PROCESS FINISHED")
print("=" * 65)
print("\nOutput directory:")
print(OUTPUT_DIR)
print("\nExisting files were not overwritten.")
