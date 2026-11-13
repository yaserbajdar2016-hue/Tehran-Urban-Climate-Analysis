
# ============================================================
# TEHRAN URBAN CLIMATE ANALYSIS
# STAGE 12: SPATIAL REGRESSION ANALYSIS
# Study year: 2024
# Sample size: 5000
# Models: OLS, GM_Lag, GM_Error_Het
# ============================================================


# ------------------------------------------------------------
# 0. IMPORT LIBRARIES
# ------------------------------------------------------------

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.metrics import mean_squared_error, mean_absolute_error

from pyproj import Transformer
from libpysal.weights import KNN
from esda.moran import Moran

import spreg


# ------------------------------------------------------------
# 1. PROJECT CONFIGURATION
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "data" / "samples" /
    "tehran_stage06_sample_2024.csv"
)

OUTPUT_DIR = (
    BASE_DIR / "results" / "spatial_regression"
)

FIGURE_DIR = OUTPUT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

STUDY_YEAR = 2024
EXPECTED_N = 5000
K_NEIGHBORS = 8
PERMUTATIONS = 999

PREDICTORS = ["NDVI", "NDBI"]
DEPENDENT = "LST_C"

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 12: SPATIAL REGRESSION")
print("=" * 70)

print("\n[1] Loading dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

required = [
    "year", "lon", "lat",
    "NDVI", "NDBI", "LST_C"
]

missing_columns = set(required) - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

df = df[required].copy()

for col in required:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

if df.isna().any().any():
    raise ValueError("Missing values detected.")

if not np.isfinite(
    df.to_numpy(dtype=float)
).all():
    raise ValueError("Non-finite values detected.")

if not (df["year"] == STUDY_YEAR).all():
    raise ValueError("Unexpected study year.")

if len(df) != EXPECTED_N:
    warnings.warn(
        f"Expected {EXPECTED_N} observations; "
        f"found {len(df)}."
    )

if df.duplicated().any():
    raise ValueError("Duplicate records detected.")

print("Observations:", len(df))
print("Variables:", PREDICTORS)
print("Dependent variable:", DEPENDENT)


# ------------------------------------------------------------
# 3. PREPARE SPATIAL COORDINATES
# ------------------------------------------------------------

print("\n[2] Preparing spatial coordinates...")

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32639",
    always_xy=True
)

x_utm, y_utm = transformer.transform(
    df["lon"].to_numpy(),
    df["lat"].to_numpy()
)

coordinates = np.column_stack([
    x_utm,
    y_utm
])

if not np.isfinite(coordinates).all():
    raise ValueError(
        "Invalid projected coordinates."
    )

if len(np.unique(coordinates, axis=0)) != len(df):
    raise ValueError(
        "Duplicate spatial coordinates detected."
    )

print("Coordinate system: EPSG:32639")
print("Spatial observations:", len(coordinates))


# ------------------------------------------------------------
# 4. CONSTRUCT KNN SPATIAL WEIGHTS
# ------------------------------------------------------------

print("\n[3] Constructing KNN spatial weights...")

if len(df) <= K_NEIGHBORS:
    raise ValueError(
        "Insufficient observations for KNN."
    )

weights = KNN.from_array(
    coordinates,
    k=K_NEIGHBORS
)

weights.transform = "R"

if weights.islands:
    raise ValueError(
        f"Isolated observations detected: "
        f"{weights.islands}"
    )

print("KNN neighbors:", K_NEIGHBORS)
print("Weight transformation: Row-standardized")
print("Number of observations:", weights.n)
print("Number of islands:", len(weights.islands))

if weights.n != len(df):
    raise ValueError(
        "Spatial weights and dataset sizes do not match."
    )

weights_metadata = pd.DataFrame([{
    "Observations": weights.n,
    "K_Neighbors": K_NEIGHBORS,
    "Transformation": "Row-standardized",
    "Coordinate_System": "EPSG:32639",
    "Islands": len(weights.islands)
}])

weights_metadata.to_csv(
    OUTPUT_DIR / "spatial_weights_metadata.csv",
    index=False
)


# ------------------------------------------------------------
# 5. PREPARE MODEL MATRICES
# ------------------------------------------------------------

print("\n[4] Preparing regression matrices...")

y = df[[DEPENDENT]].to_numpy(dtype=float)

X = df[PREDICTORS].to_numpy(dtype=float)

print("Dependent variable shape:", y.shape)
print("Predictor matrix shape:", X.shape)


# ------------------------------------------------------------
# 6. OLS BASELINE MODEL
# ------------------------------------------------------------

print("\n[5] Estimating OLS baseline...")

X_ols = sm.add_constant(
    df[PREDICTORS],
    has_constant="add"
)

ols = sm.OLS(
    df[DEPENDENT],
    X_ols
).fit()

print(ols.summary())

ols_residuals = (
    df[DEPENDENT].to_numpy() -
    ols.predict(X_ols).to_numpy()
)


# ------------------------------------------------------------
# 7. SPATIAL LAG MODEL - GM_LAG
# ------------------------------------------------------------

print("\n[6] Estimating Spatial Lag Model...")

spatial_lag = spreg.GM_Lag(
    y,
    X,
    w=weights,
    w_lags=1,
    robust="white",
    name_y=DEPENDENT,
    name_x=PREDICTORS
)

print(spatial_lag.summary)


# ------------------------------------------------------------
# 8. SPATIAL ERROR MODEL - GM_ERROR_HET
# ------------------------------------------------------------

print("\n[7] Estimating Spatial Error Model...")

spatial_error = spreg.GM_Error_Het(
    y,
    X,
    w=weights,
    name_y=DEPENDENT,
    name_x=PREDICTORS
)

print(spatial_error.summary)


# ------------------------------------------------------------
# 9. MODEL PERFORMANCE
# ------------------------------------------------------------

print("\n[8] Calculating model performance...")


def calculate_metrics(
    name,
    observed,
    predicted,
    residuals,
    r2
):

    observed = np.asarray(
        observed
    ).reshape(-1)

    predicted = np.asarray(
        predicted
    ).reshape(-1)

    residuals = np.asarray(
        residuals
    ).reshape(-1)

    return {
        "Model": name,
        "N": len(observed),

        "R_squared_or_Pseudo_R_squared": r2,

        "RMSE": np.sqrt(
            mean_squared_error(
                observed,
                predicted
            )
        ),

        "MAE": mean_absolute_error(
            observed,
            predicted
        ),

        "Residual_Mean": np.mean(
            residuals
        ),

        "Residual_SD": np.std(
            residuals,
            ddof=1
        )
    }


results = []

results.append(
    calculate_metrics(
        "OLS",
        y,
        ols.fittedvalues,
        ols_residuals,
        ols.rsquared
    )
)

for name, model in [
    ("GM_Lag", spatial_lag),
    ("GM_Error_Het", spatial_error)
]:

    residuals = np.asarray(
        model.u
    ).reshape(-1)

    predictions = np.asarray(
        model.predy
    ).reshape(-1)

    results.append(
        calculate_metrics(
            name,
            y,
            predictions,
            residuals,
            getattr(
                model,
                "pr2",
                np.nan
            )
        )
    )


metrics = pd.DataFrame(results)

metrics.to_csv(
    OUTPUT_DIR /
    "spatial_regression_model_metrics.csv",
    index=False
)

print(
    metrics.round(5).to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 10. RESIDUAL SPATIAL AUTOCORRELATION
# ------------------------------------------------------------

print("\n[9] Residual Moran's I analysis...")

residual_models = {

    "OLS": ols_residuals,

    "GM_Lag": np.asarray(
        spatial_lag.u
    ).reshape(-1),

    "GM_Error_Het": np.asarray(
        spatial_error.u
    ).reshape(-1)

}

moran_results = []

for name, residuals in residual_models.items():

    moran = Moran(
        residuals,
        weights,
        permutations=PERMUTATIONS,
        two_tailed=True
    )

    moran_results.append({

        "Model": name,

        "Moran_I": moran.I,

        "Expected_I": moran.EI,

        "P_Value": moran.p_sim,

        "Z_Score": moran.z_sim,

        "Permutations": PERMUTATIONS

    })

    print(
        f"{name}: Moran's I = "
        f"{moran.I:.6f}, "
        f"p = {moran.p_sim:.6f}"
    )


moran_df = pd.DataFrame(
    moran_results
)

moran_df.to_csv(
    OUTPUT_DIR /
    "spatial_regression_residual_moran.csv",
    index=False
)


# ------------------------------------------------------------
# 11. SAVE RESIDUAL DATASETS
# ------------------------------------------------------------

print("\n[10] Saving residual datasets...")

for name, residuals in residual_models.items():

    residual_output = df.copy()

    residual_output["Residual"] = residuals

    residual_output.to_csv(
        OUTPUT_DIR /
        f"{name.lower()}_residuals.csv",
        index=False
    )

    print(
        f"Saved: {name.lower()}_residuals.csv"
    )


# ------------------------------------------------------------
# 12. SAVE MODEL SUMMARIES
# ------------------------------------------------------------

print("\n[11] Saving model summaries...")

for name, model in [

    ("OLS", ols),

    ("GM_Lag", spatial_lag),

    ("GM_Error_Het", spatial_error)

]:

    summary_file = (
        OUTPUT_DIR /
        f"{name.lower()}_summary.txt"
    )

    summary_attribute = model.summary

    if callable(summary_attribute):

        summary_text = str(
            summary_attribute()
        )

    else:

        summary_text = str(
            summary_attribute
        )

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary_text)

    print(
        f"Saved: {summary_file.name}"
    )


# Save model comparison

metrics.to_csv(
    OUTPUT_DIR /
    "model_comparison.csv",
    index=False
)

print("Saved: model_comparison.csv")


# ------------------------------------------------------------
# 13. FINAL REPORT
# ------------------------------------------------------------

print("\n[12] Generating final report...")

report_file = (
    OUTPUT_DIR /
    "stage12_summary.txt"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "TEHRAN URBAN CLIMATE ANALYSIS\n"
    )

    f.write(
        "STAGE 12: SPATIAL REGRESSION\n\n"
    )

    f.write(
        f"Study year: {STUDY_YEAR}\n"
    )

    f.write(
        f"Observations: {len(df)}\n"
    )

    f.write(
        f"Spatial weights: KNN ({K_NEIGHBORS})\n"
    )

    f.write(
        "Weight transformation: Row-standardized\n"
    )

    f.write(
        "Coordinate system: EPSG:32639\n\n"
    )

    f.write("MODELS\n")

    f.write("1. OLS baseline\n")

    f.write("2. Spatial Lag: GM_Lag\n")

    f.write("3. Spatial Error: GM_Error_Het\n\n")

    f.write("MODEL PERFORMANCE\n")

    f.write(
        metrics.to_string(index=False)
    )

    f.write("\n\nRESIDUAL MORAN'S I\n")

    f.write(
        moran_df.to_string(index=False)
    )

    f.write(
        "\n\nInterpretation must consider estimator "
        "assumptions, spatial weights specification, "
        "and residual diagnostics.\n"
    )

print(
    f"Saved: {report_file.name}"
)


# ------------------------------------------------------------
# 14. FINAL OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 70)

print(
    "STAGE 12 COMPLETED SUCCESSFULLY"
)

print("=" * 70)

print("\nOutput directory:")

print(OUTPUT_DIR)

print("\nGenerated files:")

for file in sorted(
    OUTPUT_DIR.glob("*")
):

    if file.is_file():

        print(file.name)

print("\n" + "=" * 70)
