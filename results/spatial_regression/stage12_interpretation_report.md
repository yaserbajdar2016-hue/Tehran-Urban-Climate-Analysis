# Tehran Urban Climate Analysis
## Stage 12: Spatial Regression Analysis and Interpretation

**Project:** Tehran Urban Climate Analysis  
**Project Owner:** Yaser Bazhdar  
**Study Year:** 2024  
**Sample Size:** 5,000 observations  
**Analysis Stage:** 12 – Spatial Regression

---

### 1. Objective

The objective of Stage 12 was to investigate spatial dependence in the relationship between land surface temperature (LST) and two satellite-derived environmental indicators: NDVI and NDBI.

Three regression approaches were implemented:

1. Ordinary Least Squares (OLS)
2. Spatial Lag Model (GM_Lag)
3. Spatial Error Model (GM_Error_Het)

The analysis aimed to assess whether incorporating spatial dependence improves model performance and reduces spatial autocorrelation in model residuals.

### 2. Data and Spatial Configuration

The analysis used 5,000 spatial observations for 2024.

- Dependent variable: LST_C
- Independent variables: NDVI and NDBI
- Coordinate reference system: EPSG:32639
- Spatial weights: K-Nearest Neighbors (KNN)
- Number of neighbors: 8
- Weight transformation: Row-standardized
- Number of spatial islands: 0

The spatial weights matrix was constructed using projected coordinates to represent neighborhood relationships between sampled locations.

### 3. Regression Results

#### 3.1 Ordinary Least Squares

The OLS model produced an R-squared of approximately 0.098.

Both NDVI and NDBI showed statistically significant positive coefficients:

- NDVI: 5.1734 (p < 0.001)
- NDBI: 24.0776 (p < 0.001)

The model RMSE was 3.830 and MAE was 3.249.

The relatively low R-squared indicates that the two explanatory variables alone account for a limited proportion of the observed variation in LST.

#### 3.2 Spatial Lag Model

The GM_Lag model identified a strong and statistically significant spatial lag coefficient:

- Spatial autoregressive coefficient (rho): 0.8056
- NDVI coefficient: 3.1658
- NDBI coefficient: 12.8962
- Pseudo R-squared: 0.7357
- Spatial pseudo R-squared: 0.1866
- RMSE: 2.136
- MAE: 1.685

The significant spatial lag coefficient indicates substantial spatial dependence in land surface temperature.

The model also produced lower in-sample RMSE and MAE values compared with OLS and the spatial error model.

The Anselin-Kelejian test returned a p-value of 0.1359. This result does not provide sufficient evidence to reject its null hypothesis under the test assumptions. However, residual Moran's I remained statistically significant, so further residual diagnostics are necessary.

#### 3.3 Spatial Error Model

The GM_Error_Het model produced the following results:

- Spatial error coefficient (lambda): 0.8833
- NDVI coefficient: 2.1926
- NDBI coefficient: 11.4803
- Pseudo R-squared: 0.0977
- RMSE: 3.884
- MAE: 3.286

The spatial error coefficient was statistically significant. Nevertheless, this model did not improve the residual spatial autocorrelation or in-sample error metrics relative to OLS.

The estimator output also indicated that Step1c was not computed. This implementation detail should be considered when interpreting the model.

### 4. Residual Spatial Autocorrelation

Global Moran's I was calculated for the residuals of all three models using 999 permutations.

| Model | Moran's I | Z-score | P-value |
|---|---:|---:|---:|
| OLS | 0.6853 | 103.82 | 0.001 |
| GM_Lag | 0.0354 | 5.24 | 0.001 |
| GM_Error_Het | 0.7139 | 104.23 | 0.001 |

The OLS residuals exhibited strong positive spatial autocorrelation.

The GM_Lag model substantially reduced the Moran's I statistic. However, its residuals still showed statistically significant spatial autocorrelation.

The GM_Error_Het model retained strong positive residual spatial autocorrelation.

The reported permutation p-value of 0.001 represents the lower resolution of the 999-permutation test and should not be interpreted as an exact probability.

These results indicate that spatial dependence is an important characteristic of the study data and is not completely accounted for by the current model specifications.

### 5. Comparative Model Assessment

The GM_Lag model achieved the lowest in-sample RMSE and MAE among the three estimated models.

However, the OLS R-squared and spatial models' pseudo R-squared values are not directly comparable because they are based on different model definitions.

Furthermore, the current error metrics are based on the estimation sample and do not represent independent predictive validation.

Therefore, GM_Lag is considered the most promising model among the three approaches tested in this stage, rather than a fully validated predictive model.

### 6. Environmental Interpretation

The positive coefficients of NDBI across the three models indicate a positive conditional association between built-up intensity and land surface temperature in the current sample.

The positive NDVI coefficients require more careful interpretation. They do not establish that vegetation increases surface temperature or that vegetation has no cooling effect.

Potential explanations requiring further investigation include:

- Relationships between vegetation distribution and other urban land-cover characteristics.
- Spatial sampling characteristics.
- Correlation between explanatory variables.
- Omitted environmental and climatic variables.
- Differences in vegetation conditions and surface properties.

The current models include only NDVI and NDBI. Consequently, the findings should be interpreted as statistical associations rather than causal effects.

### 7. Methodological Limitations

Several limitations should be considered before drawing broader conclusions:

1. Only two explanatory variables were included in the regression models.
2. Residual spatial autocorrelation remained statistically significant in all three models.
3. The KNN specification (k = 8) represents one spatial neighborhood definition and has not yet been compared with alternative specifications.
4. Model performance was assessed using the estimation sample; independent validation has not yet been conducted.
5. Spatial model pseudo R-squared values should not be directly compared with OLS R-squared.
6. The simple impacts reported for GM_Lag require further examination before being interpreted as comprehensive spatial direct and indirect effects.
7. The current analysis does not establish causal relationships between vegetation, built-up intensity, and land surface temperature.

### 8. Conclusion

Stage 12 successfully implemented and compared OLS, spatial lag, and spatial error regression models using 5,000 observations from Tehran for 2024.

The results demonstrate substantial spatial dependence in land surface temperature.

Among the tested models, GM_Lag achieved the lowest in-sample prediction errors and substantially reduced residual spatial autocorrelation. Nevertheless, statistically significant residual spatial dependence remained.

The results provide evidence that spatial regression is relevant to the analysis of urban thermal patterns in Tehran. Further diagnostic testing, alternative spatial weights specifications, and independent validation are required before selecting a final model.

### 9. Generated Outputs

The following files were generated in `results/spatial_regression/`:

- `ols_residuals.csv`
- `gm_lag_residuals.csv`
- `gm_error_het_residuals.csv`
- `ols_summary.txt`
- `gm_lag_summary.txt`
- `gm_error_het_summary.txt`
- `model_comparison.csv`
- `spatial_regression_model_metrics.csv`
- `spatial_regression_residual_moran.csv`
- `spatial_weights_metadata.csv`
- `stage12_summary.txt`

### 10. Stage Status

**Computational implementation:** Completed successfully.

**Model estimation:** Completed.

**Residual spatial autocorrelation assessment:** Completed.

**Scientific interpretation:** Documented.

**Independent validation and further spatial diagnostics:** Pending.

**Overall status:** Stage 12 computationally completed; further diagnostic validation is required before final model selection.