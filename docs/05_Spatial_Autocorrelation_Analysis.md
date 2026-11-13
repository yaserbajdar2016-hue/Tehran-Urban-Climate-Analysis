# Spatial Autocorrelation Analysis of Urban Environmental Variables in Tehran

## 1. Study Overview

This stage examines the spatial distribution and clustering patterns of three environmental variables across Tehran: Normalized Difference Vegetation Index (NDVI), Normalized Difference Built-up Index (NDBI), and Land Surface Temperature (LST).

The analysis uses 5,000 spatial samples extracted for 2024. The main objectives are to:

- Identify global spatial autocorrelation patterns.
- Detect local clusters and spatial outliers.
- Evaluate the robustness of local cluster patterns after multiple-testing correction.

## 2. Data and Spatial Configuration

| Parameter | Description |
|---|---|
| Study area | Tehran, Iran |
| Study year | 2024 |
| Number of samples | 5,000 |
| Environmental variables | NDVI, NDBI, LST_C |
| Missing values | 0 |
| Duplicate coordinates | 0 |
| Projected coordinate system | WGS 84 / UTM Zone 39N (EPSG:32639) |
| Spatial weights | K-Nearest Neighbors (KNN) |
| Number of neighbors | 8 |
| Weight transformation | Row-standardized |
| Permutations | 999 |
| Random seed | 42 |
| Significance threshold | 0.05 |

Geographic coordinates were projected to UTM Zone 39N before constructing the spatial weights matrix. A KNN structure with eight neighbors was used to represent local spatial relationships.

## 3. Global Spatial Autocorrelation

Global Moran's I was calculated independently for NDVI, NDBI, and LST_C using 999 permutation tests.

### 3.1 Results

| Variable | Moran's I | Expected I | Z-score | Pseudo p-value |
|---|---:|---:|---:|---:|
| NDVI | 0.282308 | -0.0002 | 43.0614 | 0.001 |
| NDBI | 0.254974 | -0.0002 | 37.8265 | 0.001 |
| LST_C | 0.716004 | -0.0002 | 107.3879 | 0.001 |

### 3.2 Interpretation

All three variables exhibit positive and statistically significant global spatial autocorrelation under the selected KNN spatial weights configuration.

LST_C has the highest Moran's I value (0.7160), indicating the strongest spatial clustering among the examined variables. NDVI (0.2823) and NDBI (0.2550) also show positive spatial autocorrelation, although their global clustering strength is lower.

The results indicate that the spatial distribution of these environmental variables is not random under the specified spatial weights structure.

The reported pseudo p-values are subject to the finite resolution of 999 permutations. A value of 0.001 represents the approximate minimum attainable permutation-based p-value under this configuration.

## 4. Local Spatial Autocorrelation (LISA)

Local Moran's I was used to identify spatial clusters and spatial outliers.

Four cluster categories were considered:

- High-High: Locations with high values surrounded by high values.
- Low-Low: Locations with low values surrounded by low values.
- High-Low: Locations with high values surrounded by low values.
- Low-High: Locations with low values surrounded by high values.

Local significance was initially evaluated using raw permutation p-values. To account for multiple local statistical tests, two false discovery rate correction procedures were applied separately to each environmental variable:

1. Benjamini-Hochberg (BH).
2. Benjamini-Yekutieli (BY).

The significance threshold was set to 0.05.

## 5. Comparison of LISA Results

### 5.1 Significant Cluster Counts

The following table reports the number of locations classified into the four significant LISA categories.

| Variable | Method | High-High | Low-Low | High-Low | Low-High | Significant locations |
|---|---|---:|---:|---:|---:|---:|
| NDVI | Raw | 464 | 883 | 105 | 181 | 1,633 |
| NDVI | BH | 182 | 296 | 13 | 54 | 545 |
| NDVI | BY | 0 | 0 | 0 | 0 | 0 |
| NDBI | Raw | 733 | 432 | 186 | 99 | 1,450 |
| NDBI | BH | 265 | 172 | 59 | 18 | 514 |
| NDBI | BY | 0 | 0 | 0 | 0 | 0 |
| LST_C | Raw | 1,242 | 1,364 | 66 | 74 | 2,746 |
| LST_C | BH | 1,066 | 926 | 31 | 41 | 2,064 |
| LST_C | BY | 0 | 0 | 0 | 0 | 0 |

### 5.2 Interpretation of Multiple-Testing Corrections

The Benjamini-Hochberg correction reduced the number of statistically significant local clusters for all three variables.

After BH correction:

- 10.90% of NDVI samples remained statistically significant.
- 10.28% of NDBI samples remained statistically significant.
- 41.28% of LST_C samples remained statistically significant.

The LST_C results retained a considerably larger proportion of significant locations than NDVI and NDBI.

No local clusters remained significant after the Benjamini-Yekutieli correction. This result should be interpreted in the context of the conservative nature of the BY procedure, the dependence among local spatial tests, and the limited resolution of permutation-based p-values.

The absence of BY-significant clusters does not establish the absence of local spatial structure.

## 6. Methodological Considerations and Limitations

Several methodological considerations should be acknowledged:

1. The results depend on the selected KNN spatial weights configuration (K = 8).
2. Local Moran's I involves multiple statistical tests, requiring appropriate correction procedures.
3. With 999 permutations, the minimum attainable pseudo p-value is approximately 0.001.
4. The BY correction produced no significant local clusters under the current permutation configuration.
5. Spatial autocorrelation identifies spatial dependence and clustering, but does not establish causal relationships.
6. The results reflect the selected spatial sampling design and should not automatically be interpreted as complete descriptions of every location within Tehran.

## 7. Main Findings

The analysis identified positive global spatial autocorrelation in NDVI, NDBI, and LST_C.

The strongest global clustering was observed for land surface temperature. Following Benjamini-Hochberg correction, a substantial number of local LST clusters remained statistically significant, while the corresponding proportions for NDVI and NDBI were lower.

These findings provide an initial spatial statistical basis for investigating the relationships between urban vegetation, built-up surfaces, and land surface temperature.

## 8. Further Analysis

Before finalizing the spatial autocorrelation stage, the following analyses are required:

- Increase the number of local permutation tests to improve p-value resolution.
- Evaluate sensitivity to alternative KNN configurations (K = 6, 8, and 10).
- Compare the stability of significant local clusters across spatial weights configurations.
- Finalize the methodological interpretation and spatial autocorrelation maps.

The subsequent regression analysis will investigate statistical relationships between environmental variables, subject to appropriate consideration of spatial dependence.

## 9. Output Files

Main outputs are stored in:

`results/spatial_autocorrelation/`

- `global_morans_i_results_updated.csv`
- `local_morans_i_results_FDR.csv`
- `LISA_cluster_counts_comparison.csv`
- `spatial_analysis_summary_FDR.txt`
- `LISA_NDVI_RAW_updated.png`
- `LISA_NDVI_BH_updated.png`
- `LISA_NDVI_BY_updated.png`
- `LISA_NDBI_RAW_updated.png`
- `LISA_NDBI_BH_updated.png`
- `LISA_NDBI_BY_updated.png`
- `LISA_LST_C_RAW_updated.png`
- `LISA_LST_C_BH_updated.png`
- `LISA_LST_C_BY_updated.png`

**Status:** Initial spatial autocorrelation analysis completed. Permutation and spatial weights sensitivity analyses remain pending.