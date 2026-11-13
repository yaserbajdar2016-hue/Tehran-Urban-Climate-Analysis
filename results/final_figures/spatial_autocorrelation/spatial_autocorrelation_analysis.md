# Spatial Autocorrelation Analysis
## Tehran Urban Climate Analysis – Stage 13
Study area: Tehran, Iran
Study year: 2024
### 1. Global Moran's I
| Variable | Moran's I | P-value |
|---|---:|---:|
| NDVI | 0.2823 | 0.0010 |
| NDBI | 0.2550 | 0.0010 |
| LST | 0.7160 | 0.0010 |
All three indicators show positive spatial autocorrelation.
LST has the strongest spatial clustering, followed by NDVI and NDBI.
These results indicate that similar environmental values tend to occur near one another.
Global Moran's I describes overall spatial association; it does not identify the geographic location of individual clusters.
Local cluster locations are examined using LISA.
### 2. Residual Spatial Autocorrelation
| Model | Residual Moran's I | P-value |
|---|---:|---:|
| OLS | 0.6853 | 0.0010 |
| GM_Lag | 0.0354 | 0.0010 |
| GM_Error_Het | 0.7139 | 0.0010 |
GM_Lag reduces residual Moran's I by approximately 94.8% relative to OLS.
However, its residual Moran's I remains statistically significant (p = 0.0010).
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
