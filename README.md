# Tehran Urban Climate Analysis

**A spatial analysis of urban environmental conditions in Tehran, Iran**

## About the project

This project examines the spatial variation of environmental and
climate-related conditions across Tehran. I used geospatial data,
statistical analysis and spatial modelling to explore how the variables
included in the study are distributed and how they are related across
the study area.

The work brings together exploratory analysis, spatial autocorrelation,
regression modelling and sensitivity analysis. It also includes maps and
figures prepared to help interpret the results.

## What I set out to examine

The analysis was organised around four main questions:

-   How do the environmental variables vary across the study area?
-   Are there statistical relationships between the variables?
-   Do the mapped values show spatial clustering or other patterns of
    spatial dependence?
-   How stable are the spatial results under the sensitivity tests
    carried out in the project?

These questions describe the scope of the analysis. They should not be
read as claims that every relationship is causal.

## Study area and sample

The study focuses on Tehran, Iran.

The project inventory records 5,000 rows in the following sample file:

`data/samples/tehran_stage06_sample_2024.csv`

This is the number of records in the CSV file. It has not, on the basis
of the inventory alone, been established that all records are unique or
that every record is a valid spatial observation.

## Analysis carried out

The project contains scripts and outputs for the following parts of the
workflow:

### Exploratory and statistical analysis

-   Data inspection and exploratory analysis
-   Descriptive statistics
-   Pearson and Spearman correlation results

### Spatial analysis

-   Spatial visualisation
-   Global Moran's I
-   Local Moran's I and LISA cluster analysis
-   False Discovery Rate (FDR) adjustment of local spatial statistics
-   Comparisons of local spatial clusters

### Regression analysis

The saved outputs include results for:

-   Ordinary Least Squares (OLS)
-   Generalised Method of Moments spatial lag (GM-Lag)
-   Generalised Method of Moments spatial error (GM-Error)

The project also contains model metrics, coefficient tables, residual
data and spatial-weights metadata.

### Sensitivity analysis

The sensitivity-analysis outputs cover global and local spatial
autocorrelation, LISA cluster sensitivity and cluster stability. A
written interpretation of the sensitivity analysis is also included in
the results directory.

## Project files

The project inventory completed on 12 November 2026 recorded 11 Python
scripts in the project root:

-   `01_data_inspection.py`
-   `02_exploratory_analysis.py`
-   `03_spatial_visualization.py`
-   `04_spatial_autocorrelation.py`
-   `04_spatial_autocorrelation_backup.py`
-   `05_spatial_sensitivity_analysis.py`
-   `06_regression_analysis.py`
-   `07_spatial_regression.py`
-   `13a_spatial_autocorrelation_figures.py`
-   `13b_complete_spatial_figures.py`
-   `13_final_maps.py`

The backup script is retained in the inventory. Its presence does not
mean that it is part of the main execution sequence.

The `results` directory contains organised outputs for regression,
spatial autocorrelation, spatial regression, sensitivity analysis and
final figures. The Stage 14 inventory recorded 53 Markdown, text and CSV
files within `results` and its subdirectories. This count does not
include every file type in the project.

## Software and reproducibility

The analysis is implemented through Python scripts and geospatial data
workflows. The exact Python version, package versions, input-data
sources and execution order still need to be recorded in the
repository's reproducibility documentation.

The inventory confirms that the listed files are present. It does not,
by itself, confirm that every script can be run from a clean environment
or that every model can be reproduced from the original inputs.

Before reproducing the analysis, users should check the data
requirements and paths used by each script. Source datasets may have
separate access or redistribution conditions and are not assumed to be
included in a public repository.

## Results and interpretation

The saved outputs include statistical tables, spatial-statistics
results, regression outputs, sensitivity results, maps and figures.
Interpretations should be read alongside the corresponding model outputs
and with attention to the assumptions and limitations of each method.

Spatial association does not, on its own, demonstrate causation. The
number of rows in the sample file should also not be treated as proof of
the number of unique or valid spatial observations.

## Current status

The project inventory and documentation audit (Stage 14) was completed
on 12 November 2026. The next task is to prepare a clear, reproducible
and appropriately documented version of the project for sharing.

This README is an introductory guide. Data-source details, software
versions, package dependencies, execution instructions and publication
permissions will be added only after they have been checked against the
project files.

## Author

**Yaser Bazhdar**

Landscape planning \| Environmental design engineering \| GIS and remote
sensing \| Spatial analysis
