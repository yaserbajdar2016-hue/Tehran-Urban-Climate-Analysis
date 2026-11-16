# Urban Climate Vulnerability and Green Infrastructure Assessment in Tehran
**Using Google Earth Engine and Python**

## Project Overview
This project investigates the relationship between urban development, vegetation dynamics, and Land Surface Temperature (LST) in Tehran, Iran. Using satellite remote sensing data (Landsat 8/9), spatial statistics, and regression modeling, this study identifies urban heat islands and proposes a **Heat and Green Infrastructure Priority Index (HPI)** to guide future green space interventions.

## Key Findings (Summer 2024)
*   **Surface Heating:** The average Land Surface Temperature (LST) in Tehran during summer 2024 was **44.77 °C**, with peaks up to **58.13 °C**.
*   **Vegetation Cooling:** A statistically significant negative correlation was found between vegetation (NDVI) and LST (**Pearson r = -0.247, p < 0.001**). An increase of 0.1 in NDVI reduces surface temperature by **0.88 °C**.
*   **Built-up Heating:** Built-up areas (NDBI) show a significant positive correlation with LST (**Pearson r = +0.306, p < 0.001**). An increase of 0.1 in NDBI increases surface temperature by **1.69 °C**.
*   **Spatial Clustering:** Global Moran's I for LST is **0.716**, indicating strong spatial clustering of heat zones.
*   **Priority Zones (HPI):** The HPI identified specific high-priority zones (e.g., around coordinates `51.372, 35.623`), where surface temperatures exceed 54 °C with near-zero vegetation cover.

## Technologies Used
*   **Google Earth Engine (GEE):** Data acquisition, cloud masking, LST calculation, and raster export.
*   **Python:** `pandas`, `numpy`, `geopandas`, `libpysal`, `esda`, `matplotlib`, `rasterio`.
*   **Spatial Statistics:** Global/Local Moran's I (LISA), OLS Regression, Spatial Lag/Error Models (GM-Lag, GM-Error).

## Repository Structure
*   `data/`: Contains raw CSV samples and GeoTIFF rasters.
*   `scripts/`: 15 Python scripts covering data processing, spatial analysis, and visualization.
*   `figures/`: Output maps (Continuous LST/NDVI/NDBI, LISA clusters, HPI Priority Zones).
*   `results/`: Statistical outputs and CSV tables.

## How to Reproduce
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the scripts sequentially (from `01_data_inspection.py` to `15_HPI_calculation.py`).

## Author
**Yaser Bazhdar**
MSc in Environmental Design Engineering, University of Tehran
*Research Interests: Urban Climate, Landscape Ecology, GIS & Remote Sensing.*
