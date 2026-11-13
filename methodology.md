# Methodology
## 1. Study Overview
This project examines environmental and climate-related spatial
patterns in Tehran, Iran, using exploratory data analysis,
spatial statistics, regression modelling, and sensitivity analysis.
The workflow combines statistical and spatial approaches to
investigate relationships between the variables included in the
project dataset and to examine whether their distributions and
relationships show spatial structure.
The analyses are implemented in Python.
## 2. Study Data
The project includes a working sample dataset:
`data/samples/tehran_stage06_sample_2024.csv`
The project inventory recorded 5,000 data records in this file.
This number refers to the recorded rows and should not be interpreted
as a verified count of unique or independently validated spatial
observations.
The dataset is used as an input to the project's analytical workflow.
Detailed information about the original data providers, acquisition
dates, spatial resolution, coordinate reference system, variable
definitions, and preprocessing history should be reported from the
original data documentation and processing scripts. These details
are not inferred where they have not been independently verified.
## 3. Analytical Workflow
The analysis is organised into several stages.
### 3.1. Data Inspection
The initial stage examines the available data and its structure.
It provides a basis for understanding the variables and preparing
the data for subsequent statistical and spatial analyses.
Main script:
- `01_data_inspection.py`
### 3.2. Exploratory Data Analysis
Exploratory analysis is used to examine the statistical
characteristics and distributions of the project variables.
The workflow includes descriptive summaries and exploratory
visualisations. These steps help identify patterns and potential
relationships that can be investigated further.
Main script:
- `02_exploratory_analysis.py`
### 3.3. Spatial Visualisation
Spatial visualisation is used to communicate the geographical
distribution of the analysed variables and to support the
interpretation of spatial patterns.
Main script:
- `03_spatial_visualization.py`
### 3.4. Spatial Autocorrelation
Spatial autocorrelation analysis examines whether the values
of a variable are spatially structured rather than randomly
distributed.
The project includes:
- Global Moran's I for examining overall spatial autocorrelation.
- Local spatial analysis using Local Indicators of Spatial
  Association (LISA).
- Local cluster and spatial outlier interpretation.
- False Discovery Rate (FDR) adjustment in the local
  significance analysis.
Main scripts:
- `04_spatial_autocorrelation.py`
- `13a_spatial_autocorrelation_figures.py`
The interpretation of these statistics depends on the spatial
weights specification and the input data. Those implementation
details should be taken from the relevant script and its outputs.
### 3.5. Regression Analysis
Regression analysis is used to examine statistical relationships
between the variables included in the modelling dataset.
The project includes ordinary least squares (OLS) regression
and spatial regression approaches.
The spatial regression workflow includes:
- General spatial lag modelling (GM-Lag).
- General spatial error modelling (GM-Error).
These models provide alternative ways to examine relationships
when spatial dependence may be relevant to the analysis.
Main scripts:
- `06_regression_analysis.py`
- `07_spatial_regression.py`
Model results should be interpreted in the context of the
specified dependent and explanatory variables, model assumptions,
and spatial weights used in the implementation.
### 3.6. Sensitivity Analysis
Sensitivity analysis examines how the analytical results
respond to changes in the tested model settings or assumptions.
The project includes a dedicated spatial sensitivity analysis
workflow and associated outputs.
Main scripts:
- `05_spatial_sensitivity_analysis.py`
- `13b_complete_spatial_figures.py`
The specific tested scenarios and their parameter values are
defined by the analysis script and the corresponding result files.
### 3.7. Final Mapping and Figure Preparation
The final stage organises analytical outputs into figures and
maps intended to support interpretation and communication
of the results.
Main script:
- `13_final_maps.py`
The resulting figures are organised under:
`results/final_figures/`
## 4. Software and Libraries
The analysis was developed in Python 3.13.14.
The project dependency list is provided in `requirements.txt`.
The identified third-party libraries include:
- NumPy
- pandas
- SciPy
- Matplotlib
- GeoPandas-related spatial analysis dependencies, including
  PySAL components such as libpysal and esda
- spreg
- statsmodels
- scikit-learn
- pyproj
The listed package versions describe the environment in which
the project scripts were inspected. They do not, by themselves,
demonstrate that the complete workflow has been reproduced
in a clean environment.
## 5. Interpretation and Limitations
The results should be interpreted with attention to the
following points:
1. The recorded sample size does not establish that all records
   are unique, spatially valid, or free of missing values.
2. Statistical association does not, on its own, demonstrate
   causation.
3. Spatial autocorrelation and regression results depend on
   the input data, variable definitions, and spatial weights
   specification.
4. The choice and construction of spatial weights should be
   considered when interpreting global and local spatial
   statistics and spatial regression results.
5. The sensitivity analysis should be interpreted according
   to the scenarios and parameter changes actually tested
   in the corresponding script.
6. Data provenance, preprocessing decisions, coordinate
   reference systems, and model specifications should be
   documented alongside the relevant input files and scripts
   before claiming full reproducibility.
## 6. Reproducibility
The repository includes the main analysis scripts,
organised result directories, a project README, and a
Python dependency file.
The current documentation describes the analytical workflow
and the software environment identified during project
inspection.
A complete independent reproduction of all results has not
been established solely by preparing these documentation files.
Reproduction requires access to the relevant input data,
the original processing steps, and the exact model settings
used by the scripts.
## 7. Project Structure
The main project components are:
- `data/` — project datasets and samples.
- `results/` — statistical outputs, spatial analysis results,
  sensitivity analysis, maps, and figures.
- `01_data_inspection.py` to `07_spatial_regression.py` —
  main analytical scripts.
- `13a_spatial_autocorrelation_figures.py` —
  spatial autocorrelation figures.
- `13b_complete_spatial_figures.py` —
  additional analytical figures.
- `13_final_maps.py` — final map preparation.
- `requirements.txt` — identified Python dependencies.
- `README.md` — project overview.
---
**Project:** Tehran Urban Climate Analysis  
**Author:** Yaser Bazhdar
