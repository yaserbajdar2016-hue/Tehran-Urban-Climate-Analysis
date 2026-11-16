# Scientific Report: Tehran Urban Climate Analysis

## 1. Introduction
Urban Heat Islands (UHI) pose significant challenges to urban sustainability. This study aims to quantify the relationship between vegetation (NDVI), built-up density (NDBI), and Land Surface Temperature (LST) in Tehran, and to develop a spatial priority framework for green infrastructure.

## 2. Methodology
Data was acquired from Landsat 8 and Landsat 9 (Collection 2, Level 2) for the summer of 2024 (June–September). Cloud masking was applied, and median composites were generated. A total of 5,000 random points were sampled for statistical analysis. Spatial autocorrelation was evaluated using Moran's I and LISA cluster maps. A Heat and Green Infrastructure Priority Index (HPI) was calculated using normalized LST and inverted NDVI.

## 3. Results
*   **Descriptive Statistics:** Mean LST was 44.77 °C (SD = 4.01). NDVI mean was 0.17, and NDBI mean was 0.02.
*   **Correlation:** NDVI and LST are negatively correlated (r = -0.247), while NDBI and LST are positively correlated (r = 0.306). Both are highly significant (p < 0.001).
*   **Regression:** Linear models show that NDBI has roughly twice the heating effect compared to the cooling effect of NDVI.
*   **Spatial Clustering:** Moran's I confirmed strong spatial dependence (LST Moran's I = 0.716). LISA maps revealed statistically significant hot spots in the southern and central districts.
*   **HPI Analysis:** The HPI map categorizes Tehran into 5 priority levels. "Very High Priority" zones correspond to dense built-up areas with high thermal stress and no vegetation.

## 4. Limitations & Future Work
*   **Cross-sectional nature:** The analysis focuses on a single representative summer (2024). Future work will incorporate the 2015–2025 time series.
*   **Spatial resolution:** Landsat's 30m thermal resolution (resampled to 100m for analysis) is coarse for micro-scale urban design.
*   **Causality:** Correlations do not imply causation; LST is also influenced by albedo, building height, and anthropogenic heat.

## 5. Conclusion
The integration of remote sensing and spatial statistics provides a robust framework for urban climate assessment. The HPI successfully identified priority zones for green infrastructure, demonstrating its potential as a decision-support tool for urban planners in Tehran.
