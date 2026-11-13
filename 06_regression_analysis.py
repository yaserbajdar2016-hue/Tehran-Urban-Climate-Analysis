
# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# Stage 11: Regression Analysis
# Study year: 2024
# Sample size: 5000
# ============================================================

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor


# ------------------------------------------------------------
# 1. PROJECT CONFIGURATION
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "data" / "samples" /
    "tehran_stage06_sample_2024.csv"
)

OUTPUT_DIR = BASE_DIR / "results" / "regression"
FIGURE_DIR = OUTPUT_DIR / "figures"
SUMMARY_DIR = OUTPUT_DIR / "model_summaries"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
K_NEIGHBORS = 8
PERMUTATIONS = 999

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 11: REGRESSION ANALYSIS")
print("=" * 65)

print("\n[1] Loading dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "year", "lon", "lat", "NDVI", "NDBI", "LST_C"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

for col in required_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if df[required_columns].isna().any().any():
    raise ValueError("Missing or non-numeric values detected.")

if not np.isfinite(df[required_columns].to_numpy(dtype=float)).all():
    raise ValueError("Infinite values detected.")

if len(df) != 5000:
    warnings.warn(f"Expected 5000 samples, found {len(df)}.")

if not df["lon"].between(-180, 180).all():
    raise ValueError("Invalid longitude values.")

if not df["lat"].between(-90, 90).all():
    raise ValueError("Invalid latitude values.")

if not (df["year"] == 2024).all():
    raise ValueError("Unexpected study year.")

if df.duplicated().any():
    raise ValueError("Duplicate complete records detected.")

print(f"Observations: {len(df)}")
print("Study year: 2024")
print("Data validation: successful")


# ------------------------------------------------------------
# 3. DESCRIPTIVE STATISTICS
# ------------------------------------------------------------

print("\n[2] Descriptive statistics...")

variables = ["NDVI", "NDBI", "LST_C"]

descriptive = df[variables].describe().T

descriptive.to_csv(
    OUTPUT_DIR / "regression_descriptive_statistics.csv"
)

print(descriptive.round(4))


# ------------------------------------------------------------
# 4. REGRESSION MODELS
# ------------------------------------------------------------

print("\n[3] Fitting regression models...")

y = df["LST_C"]

model_definitions = {
    "Model_1_NDVI": ["NDVI"],
    "Model_2_NDBI": ["NDBI"],
    "Model_3_Multivariate": ["NDVI", "NDBI"]
}

models = {}
metrics = []
coefficient_results = []

for model_name, predictors in model_definitions.items():

    print(f"\nFitting {model_name}...")

    X = sm.add_constant(df[predictors])

    model = sm.OLS(y, X).fit()
    robust_model = model.get_robustcov_results(cov_type="HC3")

    models[model_name] = model

    predictions = model.predict(X)
    residuals = y - predictions

    rmse = np.sqrt(mean_squared_error(y, predictions))
    mae = mean_absolute_error(y, predictions)

    metrics.append({
        "Model": model_name,
        "Predictors": " + ".join(predictors),
        "N": int(model.nobs),
        "R_squared": model.rsquared,
        "Adjusted_R_squared": model.rsquared_adj,
        "RMSE": rmse,
        "MAE": mae,
        "AIC": model.aic,
        "BIC": model.bic
    })

    conventional_ci = model.conf_int()
    robust_ci = robust_model.conf_int()

    for i, term in enumerate(model.params.index):

        coefficient_results.append({
            "Model": model_name,
            "Term": term,
            "Coefficient": model.params[term],
            "Conventional_SE": model.bse[term],
            "Conventional_P_Value": model.pvalues[term],
            "Conventional_CI_Lower": conventional_ci.loc[term, 0],
            "Conventional_CI_Upper": conventional_ci.loc[term, 1],
            "HC3_SE": robust_model.bse[i],
            "HC3_P_Value": robust_model.pvalues[i],
            "HC3_CI_Lower": robust_ci[i, 0],
            "HC3_CI_Upper": robust_ci[i, 1]
        })

    with open(
        SUMMARY_DIR / f"{model_name}_summary.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("CONVENTIONAL OLS RESULTS\n")
        f.write("=" * 60 + "\n")
        f.write(model.summary().as_text())

        f.write("\n\nHC3 ROBUST INFERENCE\n")
        f.write("=" * 60 + "\n")
        f.write(robust_model.summary().as_text())


metrics_df = pd.DataFrame(metrics)

metrics_df.to_csv(
    OUTPUT_DIR / "regression_model_metrics.csv",
    index=False
)

coefficients_df = pd.DataFrame(coefficient_results)

coefficients_df.to_csv(
    OUTPUT_DIR / "regression_coefficients.csv",
    index=False
)

print("\nMODEL PERFORMANCE:")
print(metrics_df.round(4).to_string(index=False))


# ------------------------------------------------------------
# 5. MODEL DIAGNOSTICS
# ------------------------------------------------------------

print("\n[4] Regression diagnostics...")

diagnostic_results = []

for model_name, model in models.items():

    residuals = model.resid

    bp_stat, bp_pvalue, _, _ = het_breuschpagan(
        residuals,
        model.model.exog
    )

    jb_stat, jb_pvalue = stats.jarque_bera(residuals)

    diagnostic_results.append({
        "Model": model_name,
        "Breusch_Pagan_Statistic": bp_stat,
        "Breusch_Pagan_P_Value": bp_pvalue,
        "Jarque_Bera_Statistic": jb_stat,
        "Jarque_Bera_P_Value": jb_pvalue
    })


diagnostics_df = pd.DataFrame(diagnostic_results)

diagnostics_df.to_csv(
    OUTPUT_DIR / "regression_diagnostics.csv",
    index=False
)

print("\nDIAGNOSTIC RESULTS:")
print(diagnostics_df.round(5).to_string(index=False))


# ------------------------------------------------------------
# 6. MULTICOLLINEARITY: VIF
# ------------------------------------------------------------

print("\n[5] Multicollinearity analysis...")

X_vif = sm.add_constant(df[["NDVI", "NDBI"]])

vif_results = []

for i, variable in enumerate(X_vif.columns):

    if variable == "const":
        continue

    vif_value = variance_inflation_factor(
        X_vif.to_numpy(),
        i
    )

    vif_results.append({
        "Variable": variable,
        "VIF": vif_value
    })

vif_df = pd.DataFrame(vif_results)

vif_df.to_csv(
    OUTPUT_DIR / "multicollinearity_vif.csv",
    index=False
)

print(vif_df.round(5).to_string(index=False))


# ------------------------------------------------------------
# 7. SAVE MODEL 3 RESIDUALS
# ------------------------------------------------------------

print("\n[6] Saving model 3 residuals...")

model3 = models["Model_3_Multivariate"]

X3 = sm.add_constant(df[["NDVI", "NDBI"]])

predictions = model3.predict(X3)

residual_dataset = df[
    ["year", "lon", "lat", "NDVI", "NDBI", "LST_C"]
].copy()

residual_dataset["Fitted_LST_C"] = predictions
residual_dataset["Residual"] = model3.resid

residual_dataset.to_csv(
    OUTPUT_DIR / "model3_residuals.csv",
    index=False
)


# ------------------------------------------------------------
# 8. SPATIAL AUTOCORRELATION OF RESIDUALS
# ------------------------------------------------------------

print("\n[7] Spatial autocorrelation of residuals...")

moran_result = {
    "Variable": "Model_3_Residuals",
    "K_Neighbors": K_NEIGHBORS,
    "Permutations": PERMUTATIONS,
    "Moran_I": np.nan,
    "Expected_I": np.nan,
    "P_Value": np.nan,
    "Status": "Not calculated"
}

try:

    from pyproj import Transformer
    from libpysal.weights import KNN
    from esda.moran import Moran

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:32639",
        always_xy=True
    )

    x_utm, y_utm = transformer.transform(
        df["lon"].to_numpy(),
        df["lat"].to_numpy()
    )

    coordinates = np.column_stack([x_utm, y_utm])

    weights = KNN.from_array(
        coordinates,
        k=K_NEIGHBORS
    )

    weights.transform = "R"

    moran = Moran(
        residual_dataset["Residual"].to_numpy(),
        weights,
        permutations=PERMUTATIONS,
        two_tailed=True
    )

    moran_result.update({
        "Moran_I": moran.I,
        "Expected_I": moran.EI,
        "P_Value": moran.p_sim,
        "Status": "Calculated successfully"
    })

    print(f"Residual Moran's I: {moran.I:.6f}")
    print(f"Expected Moran's I: {moran.EI:.6f}")
    print(f"Permutation p-value: {moran.p_sim:.6f}")

except ImportError as error:

    moran_result["Status"] = f"Missing spatial package: {error}"

    print("Required spatial packages are unavailable.")
    print("Install pyproj, libpysal and esda.")

except Exception as error:

    moran_result["Status"] = f"Calculation failed: {error}"

    print("Residual spatial test failed:")
    print(error)


pd.DataFrame([moran_result]).to_csv(
    OUTPUT_DIR / "residual_spatial_autocorrelation.csv",
    index=False
)


# ------------------------------------------------------------
# 9. REGRESSION RELATIONSHIP FIGURES
# ------------------------------------------------------------

print("\n[8] Generating regression relationship figures...")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

relationships = [
    ("NDVI", "Model_1_NDVI"),
    ("NDBI", "Model_2_NDBI")
]

for ax, (variable, model_name) in zip(axes, relationships):

    ax.scatter(
        df[variable],
        df["LST_C"],
        alpha=0.35,
        s=15
    )

    x_values = np.linspace(
        df[variable].min(),
        df[variable].max(),
        200
    )

    line_data = pd.DataFrame({variable: x_values})

    line_predictions = models[model_name].predict(
        sm.add_constant(line_data, has_constant="add")
    )

    ax.plot(
        x_values,
        line_predictions,
        linewidth=2
    )

    ax.set_xlabel(variable)
    ax.set_ylabel("Land Surface Temperature (°C)")

    ax.set_title(
        f"{variable} vs LST\n"
        f"R² = {models[model_name].rsquared:.3f}"
    )

    ax.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "regression_relationships.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 10. MODEL 3 RESIDUAL DIAGNOSTIC FIGURES
# ------------------------------------------------------------

print("\n[9] Generating residual diagnostic plots...")

residuals = model3.resid
fitted = model3.fittedvalues

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].scatter(
    fitted,
    residuals,
    alpha=0.35,
    s=15
)

axes[0, 0].axhline(0, linestyle="--")
axes[0, 0].set_xlabel("Fitted LST (°C)")
axes[0, 0].set_ylabel("Residuals")
axes[0, 0].set_title("Residuals vs Fitted")

axes[0, 1].hist(
    residuals,
    bins=40,
    edgecolor="black"
)

axes[0, 1].set_title("Residual Distribution")
axes[0, 1].set_xlabel("Residuals")

sm.qqplot(
    residuals,
    line="45",
    ax=axes[1, 0]
)

axes[1, 0].set_title("Normal Q-Q Plot")

axes[1, 1].scatter(
    df["LST_C"],
    fitted,
    alpha=0.35,
    s=15
)

minimum = min(df["LST_C"].min(), fitted.min())
maximum = max(df["LST_C"].max(), fitted.max())

axes[1, 1].plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

axes[1, 1].set_xlabel("Observed LST (°C)")
axes[1, 1].set_ylabel("Predicted LST (°C)")
axes[1, 1].set_title("Observed vs Predicted")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "model3_residual_diagnostics.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 11. FINAL EXECUTION REPORT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("STAGE 11 REGRESSION ANALYSIS COMPLETED")
print("=" * 65)

print("\nGenerated output files:")

for file in sorted(OUTPUT_DIR.rglob("*")):

    if file.is_file():

        print(
            file.relative_to(BASE_DIR),
            f"({file.stat().st_size:,} bytes)"
        )

print("\nImportant:")
print("- HC3 robust results are included.")
print("- Spatial residual autocorrelation must be evaluated.")
print("- Conventional OLS p-values require spatial caution.")
print("- Regression does not establish causal relationships.")

print("\nAnalysis finished.")
