# Exploratory Data Analysis – Tehran Urban Climate Analysis

## 1. Dataset Description

The exploratory analysis was conducted using 5,000 spatial samples extracted from Google Earth Engine for Tehran, Iran, for the year 2024.

The dataset included six variables: year, longitude, latitude, NDVI, NDBI, and Land Surface Temperature (LST).

No missing values were identified in the dataset.

## 2. Descriptive Statistics

| Variable | Mean | Standard Deviation |
|---|---:|---:|
| NDVI | 0.1707 | 0.1124 |
| NDBI | 0.0228 | 0.0730 |
| LST (°C) | 44.8384 | 4.0327 |

## 3. Correlation Analysis

Pearson correlation analysis revealed:

- NDVI and LST: r = -0.2467
- NDBI and LST: r = 0.3061
- NDVI and NDBI: r = -0.8975

Spearman correlation analysis showed similar directions of association.

## 4. Linear Regression

Simple linear regression produced the following R-squared values:

- NDVI and LST: R² = 0.0608
- NDBI and LST: R² = 0.0937
- NDVI and NDBI: R² = 0.8054

## 5. Preliminary Interpretation

The results indicate a negative association between vegetation greenness (NDVI) and land surface temperature, while built-up intensity (NDBI) shows a positive association with LST.

A strong negative association was also observed between NDVI and NDBI.

These findings suggest spatial relationships between vegetation, built-up surfaces, and surface thermal conditions in Tehran.

## 6. Limitations

The analysis is based on a single year (2024) and a sample of 5,000 spatial observations.

Correlation does not establish causation. Spatial autocorrelation, sampling design, and possible multicollinearity between NDVI and NDBI should be examined in subsequent analyses.

Statistical significance should also be interpreted cautiously because spatial observations may not be independent.