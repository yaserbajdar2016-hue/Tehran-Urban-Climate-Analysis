from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
# ============================================================
# STAGE 13 - ADDITIONAL SPATIAL AUTOCORRELATION FIGURES
# Tehran Urban Climate Analysis - 2024
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
FINAL_DIR = RESULTS_DIR / "final_figures"
AUTO_DIR = FINAL_DIR / "spatial_autocorrelation"
AUTO_DIR.mkdir(parents=True, exist_ok=True)
GLOBAL_FILE = (
    RESULTS_DIR / "spatial_autocorrelation" /
    "global_morans_i_results_updated.csv"
)
RESIDUAL_FILE = (
    RESULTS_DIR / "spatial_regression" /
    "spatial_regression_residual_moran.csv"
)
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.family"] = "DejaVu Sans"
def find_column(df, candidates):
    lookup = {
        str(c).strip().lower().replace(" ", "_"): c
        for c in df.columns
    }
    for candidate in candidates:
        key = candidate.strip().lower().replace(" ", "_")
        if key in lookup:
            return lookup[key]
    return None
print("\n" + "=" * 65)
print("STAGE 13 - ADDITIONAL SPATIAL FIGURES")
print("=" * 65)
summary_parts = []
# ------------------------------------------------------------
# 1. GLOBAL MORAN'S I
# ------------------------------------------------------------
if GLOBAL_FILE.exists():
    global_df = pd.read_csv(GLOBAL_FILE)
    variable_col = find_column(
        global_df, ["Variable", "Name"]
    )
    moran_col = find_column(
        global_df, ["Moran_I", "Morans_I"]
    )
    p_col = find_column(
        global_df, ["P_Value", "P_Value_Sim", "p_sim"]
    )
    z_col = find_column(
        global_df, ["Z_Score", "Z_Sim", "z_sim"]
    )
    perm_col = find_column(
        global_df, ["Permutations"]
    )
    if variable_col is not None and moran_col is not None:
        plot_df = global_df.copy()
        plot_df[moran_col] = pd.to_numeric(
            plot_df[moran_col], errors="coerce"
        )
        plot_df = plot_df.dropna(subset=[moran_col])
        fig, ax = plt.subplots(figsize=(9, 6))
        bars = ax.bar(
            plot_df[variable_col].astype(str),
            plot_df[moran_col],
            edgecolor="black",
            linewidth=0.7
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(
            "Global Spatial Autocorrelation - Tehran 2024",
            fontsize=14,
            fontweight="bold"
        )
        ax.set_ylabel("Global Moran's I")
        ax.set_xlabel("Environmental Variable")
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        for bar, (_, row) in zip(bars, plot_df.iterrows()):
            value = row[moran_col]
            label = f"{value:.3f}"
            if p_col is not None:
                p_value = pd.to_numeric(
                    pd.Series([row[p_col]]), errors="coerce"
                ).iloc[0]
                if pd.notna(p_value):
                    label += f"\np={p_value:.3g}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                label,
                ha="center",
                va="bottom",
                fontsize=9
            )
        fig.tight_layout()
        output = AUTO_DIR / "global_morans_i_comparison.png"
        fig.savefig(output, bbox_inches="tight")
        plt.close(fig)
        print("[OK] Global Moran's I figure:", output.name)
        for _, row in plot_df.iterrows():
            record = {
                "Analysis": "Global Moran's I",
                "Variable_or_Model": row[variable_col],
                "Moran_I": row[moran_col],
                "P_Value": row[p_col] if p_col else None,
                "Z_Score": row[z_col] if z_col else None,
                "Permutations": row[perm_col] if perm_col else None
            }
            summary_parts.append(record)
    else:
        print("[WARNING] Required columns not found in global Moran CSV.")
        print("Available columns:", global_df.columns.tolist())
else:
    print("[MISSING] Global Moran CSV:", GLOBAL_FILE)
# ------------------------------------------------------------
# 2. RESIDUAL MORAN'S I - REGRESSION MODELS
# ------------------------------------------------------------
if RESIDUAL_FILE.exists():
    residual_df = pd.read_csv(RESIDUAL_FILE)
    model_col = find_column(
        residual_df, ["Model", "Model_Name"]
    )
    moran_col = find_column(
        residual_df, ["Moran_I", "Residual_Morans_I", "Morans_I"]
    )
    p_col = find_column(
        residual_df, ["P_Value", "P_Value_Sim", "p_sim"]
    )
    z_col = find_column(
        residual_df, ["Z_Score", "Z_Sim", "z_sim"]
    )
    perm_col = find_column(
        residual_df, ["Permutations"]
    )
    if model_col is not None and moran_col is not None:
        plot_df = residual_df.copy()
        plot_df[moran_col] = pd.to_numeric(
            plot_df[moran_col], errors="coerce"
        )
        plot_df = plot_df.dropna(subset=[moran_col])
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(
            plot_df[model_col].astype(str),
            plot_df[moran_col],
            edgecolor="black",
            linewidth=0.7
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(
            "Residual Spatial Autocorrelation by Regression Model",
            fontsize=13,
            fontweight="bold"
        )
        ax.set_ylabel("Residual Moran's I")
        ax.set_xlabel("Regression Model")
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        for bar, (_, row) in zip(bars, plot_df.iterrows()):
            value = row[moran_col]
            label = f"{value:.3f}"
            if p_col is not None:
                p_value = pd.to_numeric(
                    pd.Series([row[p_col]]), errors="coerce"
                ).iloc[0]
                if pd.notna(p_value):
                    label += f"\np={p_value:.3g}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                label,
                ha="center",
                va="bottom",
                fontsize=9
            )
        fig.tight_layout()
        output = AUTO_DIR / "residual_morans_i_comparison.png"
        fig.savefig(output, bbox_inches="tight")
        plt.close(fig)
        print("[OK] Residual Moran's I figure:", output.name)
        for _, row in plot_df.iterrows():
            record = {
                "Analysis": "Regression residual Moran's I",
                "Variable_or_Model": row[model_col],
                "Moran_I": row[moran_col],
                "P_Value": row[p_col] if p_col else None,
                "Z_Score": row[z_col] if z_col else None,
                "Permutations": row[perm_col] if perm_col else None
            }
            summary_parts.append(record)
    else:
        print("[WARNING] Required columns not found in residual Moran CSV.")
        print("Available columns:", residual_df.columns.tolist())
else:
    print("[MISSING] Residual Moran CSV:", RESIDUAL_FILE)
# ------------------------------------------------------------
# 3. COMBINED SPATIAL STATISTICS TABLE
# ------------------------------------------------------------
if summary_parts:
    summary_df = pd.DataFrame(summary_parts)
    summary_path = AUTO_DIR / "final_spatial_autocorrelation_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print("[OK] Spatial summary CSV:", summary_path.name)
else:
    print("[WARNING] No spatial summary table was generated.")
# ------------------------------------------------------------
# 4. COMPLETE STAGE 13 FILE INVENTORY
# ------------------------------------------------------------
inventory = []
for file_path in FINAL_DIR.rglob("*"):
    if file_path.is_file():
        inventory.append({
            "Category": file_path.parent.name,
            "Filename": file_path.name,
            "Relative_Path": str(file_path.relative_to(FINAL_DIR)),
            "Size_KB": round(file_path.stat().st_size / 1024, 2)
        })
inventory_df = pd.DataFrame(inventory)
inventory_path = FINAL_DIR / "stage13_complete_output_inventory.csv"
inventory_df.to_csv(inventory_path, index=False)
# ------------------------------------------------------------
# 5. FINAL SUMMARY REPORT
# ------------------------------------------------------------
report_path = FINAL_DIR / "STAGE13_COMPLETION_REPORT.txt"
with open(report_path, "w", encoding="utf-8") as report:
    report.write("TEHRAN URBAN CLIMATE ANALYSIS\n")
    report.write("STAGE 13 - FINAL MAPS AND FIGURES\n")
    report.write("=" * 60 + "\n\n")
    report.write("Study area: Tehran, Iran\n")
    report.write("Study year: 2024\n")
    report.write("Project owner: Yaser Bazhdar\n\n")
    report.write("Final output categories:\n")
    for folder in sorted(FINAL_DIR.iterdir()):
        if folder.is_dir():
            count = sum(1 for p in folder.rglob("*") if p.is_file())
            report.write(f"- {folder.name}: {count} files\n")
    report.write(f"\nTotal files inventoried: {len(inventory_df)}\n")
    report.write("\nStage 13 supplementary spatial figures:\n")
    report.write("- Global Moran's I comparison\n")
    report.write("- Regression residual Moran's I comparison\n")
    report.write("- Spatial autocorrelation summary CSV\n")
    report.write("\nOriginal Stage 1-12 data and scripts were not modified.\n")
print("[OK] Complete inventory:", inventory_path.name)
print("[OK] Completion report:", report_path.name)
print("\n" + "=" * 65)
print("STAGE 13 SUPPLEMENTARY OUTPUTS COMPLETED")
print("=" * 65)
print("Files inventoried:", len(inventory_df))
print("Final directory:", FINAL_DIR)
print("\nNew spatial autocorrelation outputs:")
for file_path in sorted(AUTO_DIR.iterdir()):
    if file_path.is_file():
        print("-", file_path.name)
