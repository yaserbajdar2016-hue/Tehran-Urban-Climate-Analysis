# Tehran Urban Climate Analysis

## Spatial Sensitivity Analysis

### Study configuration

- Samples: 5000
- Study year: 2024
- Variables: NDVI, NDBI, LST_C
- KNN configurations: 6, 8, 10
- Permutations: 4999
- Random seed base: 42
- Coordinate system: EPSG:32639
- Weight transformation: Row-standardized
- FDR: BH and BY
- Significance threshold: 0.05

### Global Moran's I results

| Variable   |   K_Neighbors |   Samples |   Moran_I |   Expected_I |   Z_Score |   P_Value | Significant   |   Permutations |   Random_Seed |
|:-----------|--------------:|----------:|----------:|-------------:|----------:|----------:|:--------------|---------------:|--------------:|
| NDVI       |             6 |      5000 |  0.310933 |  -0.00020004 |   40.0377 |    0.0002 | True          |           4999 |            48 |
| NDBI       |             6 |      5000 |  0.279526 |  -0.00020004 |   35.7157 |    0.0002 | True          |           4999 |            48 |
| LST_C      |             6 |      5000 |  0.744297 |  -0.00020004 |   95.9498 |    0.0002 | True          |           4999 |            48 |
| NDVI       |             8 |      5000 |  0.282308 |  -0.00020004 |   41.3534 |    0.0002 | True          |           4999 |            50 |
| NDBI       |             8 |      5000 |  0.254974 |  -0.00020004 |   36.9276 |    0.0002 | True          |           4999 |            50 |
| LST_C      |             8 |      5000 |  0.716004 |  -0.00020004 |  106.814  |    0.0002 | True          |           4999 |            50 |
| NDVI       |            10 |      5000 |  0.258208 |  -0.00020004 |   43.1169 |    0.0002 | True          |           4999 |            52 |
| NDBI       |            10 |      5000 |  0.232977 |  -0.00020004 |   39.2161 |    0.0002 | True          |           4999 |            52 |
| LST_C      |            10 |      5000 |  0.695002 |  -0.00020004 |  115.712  |    0.0002 | True          |           4999 |            52 |

### LISA cluster sensitivity

| Variable   |   K_Neighbors | Method   | Cluster         |   Count |   Percentage |
|:-----------|--------------:|:---------|:----------------|--------:|-------------:|
| NDVI       |             6 | Raw      | High-High       |     432 |         8.64 |
| NDVI       |             6 | Raw      | Low-Low         |     798 |        15.96 |
| NDVI       |             6 | Raw      | High-Low        |      77 |         1.54 |
| NDVI       |             6 | Raw      | Low-High        |     176 |         3.52 |
| NDVI       |             6 | Raw      | Not Significant |    3517 |        70.34 |
| NDVI       |             6 | BH       | High-High       |     112 |         2.24 |
| NDVI       |             6 | BH       | Low-Low         |     149 |         2.98 |
| NDVI       |             6 | BH       | High-Low        |       6 |         0.12 |
| NDVI       |             6 | BH       | Low-High        |      15 |         0.3  |
| NDVI       |             6 | BH       | Not Significant |    4718 |        94.36 |
| NDVI       |             6 | BY       | High-High       |       0 |         0    |
| NDVI       |             6 | BY       | Low-Low         |       0 |         0    |
| NDVI       |             6 | BY       | High-Low        |       0 |         0    |
| NDVI       |             6 | BY       | Low-High        |       0 |         0    |
| NDVI       |             6 | BY       | Not Significant |    5000 |       100    |
| NDVI       |             8 | Raw      | High-High       |     493 |         9.86 |
| NDVI       |             8 | Raw      | Low-Low         |     846 |        16.92 |
| NDVI       |             8 | Raw      | High-Low        |      97 |         1.94 |
| NDVI       |             8 | Raw      | Low-High        |     209 |         4.18 |
| NDVI       |             8 | Raw      | Not Significant |    3355 |        67.1  |
| NDVI       |             8 | BH       | High-High       |     182 |         3.64 |
| NDVI       |             8 | BH       | Low-Low         |     307 |         6.14 |
| NDVI       |             8 | BH       | High-Low        |      17 |         0.34 |
| NDVI       |             8 | BH       | Low-High        |      57 |         1.14 |
| NDVI       |             8 | BH       | Not Significant |    4437 |        88.74 |
| NDVI       |             8 | BY       | High-High       |       0 |         0    |
| NDVI       |             8 | BY       | Low-Low         |       0 |         0    |
| NDVI       |             8 | BY       | High-Low        |       0 |         0    |
| NDVI       |             8 | BY       | Low-High        |       0 |         0    |
| NDVI       |             8 | BY       | Not Significant |    5000 |       100    |
| NDVI       |            10 | Raw      | High-High       |     531 |        10.62 |
| NDVI       |            10 | Raw      | Low-Low         |     945 |        18.9  |
| NDVI       |            10 | Raw      | High-Low        |     112 |         2.24 |
| NDVI       |            10 | Raw      | Low-High        |     253 |         5.06 |
| NDVI       |            10 | Raw      | Not Significant |    3159 |        63.18 |
| NDVI       |            10 | BH       | High-High       |     266 |         5.32 |
| NDVI       |            10 | BH       | Low-Low         |     502 |        10.04 |
| NDVI       |            10 | BH       | High-Low        |      49 |         0.98 |
| NDVI       |            10 | BH       | Low-High        |      91 |         1.82 |
| NDVI       |            10 | BH       | Not Significant |    4092 |        81.84 |
| NDVI       |            10 | BY       | High-High       |       0 |         0    |
| NDVI       |            10 | BY       | Low-Low         |       0 |         0    |
| NDVI       |            10 | BY       | High-Low        |       0 |         0    |
| NDVI       |            10 | BY       | Low-High        |       0 |         0    |
| NDVI       |            10 | BY       | Not Significant |    5000 |       100    |
| NDBI       |             6 | Raw      | High-High       |     682 |        13.64 |
| NDBI       |             6 | Raw      | Low-Low         |     402 |         8.04 |
| NDBI       |             6 | Raw      | High-Low        |     180 |         3.6  |
| NDBI       |             6 | Raw      | Low-High        |      84 |         1.68 |
| NDBI       |             6 | Raw      | Not Significant |    3652 |        73.04 |
| NDBI       |             6 | BH       | High-High       |     196 |         3.92 |
| NDBI       |             6 | BH       | Low-Low         |     110 |         2.2  |
| NDBI       |             6 | BH       | High-Low        |      30 |         0.6  |
| NDBI       |             6 | BH       | Low-High        |       7 |         0.14 |
| NDBI       |             6 | BH       | Not Significant |    4657 |        93.14 |
| NDBI       |             6 | BY       | High-High       |       0 |         0    |
| NDBI       |             6 | BY       | Low-Low         |       0 |         0    |
| NDBI       |             6 | BY       | High-Low        |       0 |         0    |
| NDBI       |             6 | BY       | Low-High        |       0 |         0    |
| NDBI       |             6 | BY       | Not Significant |    5000 |       100    |
| NDBI       |             8 | Raw      | High-High       |     737 |        14.74 |
| NDBI       |             8 | Raw      | Low-Low         |     460 |         9.2  |
| NDBI       |             8 | Raw      | High-Low        |     207 |         4.14 |
| NDBI       |             8 | Raw      | Low-High        |     103 |         2.06 |
| NDBI       |             8 | Raw      | Not Significant |    3493 |        69.86 |
| NDBI       |             8 | BH       | High-High       |     275 |         5.5  |
| NDBI       |             8 | BH       | Low-Low         |     150 |         3    |
| NDBI       |             8 | BH       | High-Low        |      49 |         0.98 |
| NDBI       |             8 | BH       | Low-High        |      19 |         0.38 |
| NDBI       |             8 | BH       | Not Significant |    4507 |        90.14 |
| NDBI       |             8 | BY       | High-High       |       0 |         0    |
| NDBI       |             8 | BY       | Low-Low         |       0 |         0    |
| NDBI       |             8 | BY       | High-Low        |       0 |         0    |
| NDBI       |             8 | BY       | Low-High        |       0 |         0    |
| NDBI       |             8 | BY       | Not Significant |    5000 |       100    |
| NDBI       |            10 | Raw      | High-High       |     805 |        16.1  |
| NDBI       |            10 | Raw      | Low-Low         |     502 |        10.04 |
| NDBI       |            10 | Raw      | High-Low        |     249 |         4.98 |
| NDBI       |            10 | Raw      | Low-High        |     113 |         2.26 |
| NDBI       |            10 | Raw      | Not Significant |    3331 |        66.62 |
| NDBI       |            10 | BH       | High-High       |     362 |         7.24 |
| NDBI       |            10 | BH       | Low-Low         |     222 |         4.44 |
| NDBI       |            10 | BH       | High-Low        |      81 |         1.62 |
| NDBI       |            10 | BH       | Low-High        |      40 |         0.8  |
| NDBI       |            10 | BH       | Not Significant |    4295 |        85.9  |
| NDBI       |            10 | BY       | High-High       |       0 |         0    |
| NDBI       |            10 | BY       | Low-Low         |       0 |         0    |
| NDBI       |            10 | BY       | High-Low        |       0 |         0    |
| NDBI       |            10 | BY       | Low-High        |       0 |         0    |
| NDBI       |            10 | BY       | Not Significant |    5000 |       100    |
| LST_C      |             6 | Raw      | High-High       |    1132 |        22.64 |
| LST_C      |             6 | Raw      | Low-Low         |    1069 |        21.38 |
| LST_C      |             6 | Raw      | High-Low        |      29 |         0.58 |
| LST_C      |             6 | Raw      | Low-High        |      39 |         0.78 |
| LST_C      |             6 | Raw      | Not Significant |    2731 |        54.62 |
| LST_C      |             6 | BH       | High-High       |     897 |        17.94 |
| LST_C      |             6 | BH       | Low-Low         |     693 |        13.86 |
| LST_C      |             6 | BH       | High-Low        |      11 |         0.22 |
| LST_C      |             6 | BH       | Low-High        |      21 |         0.42 |
| LST_C      |             6 | BH       | Not Significant |    3378 |        67.56 |
| LST_C      |             6 | BY       | High-High       |     406 |         8.12 |
| LST_C      |             6 | BY       | Low-Low         |     325 |         6.5  |
| LST_C      |             6 | BY       | High-Low        |       1 |         0.02 |
| LST_C      |             6 | BY       | Low-High        |       1 |         0.02 |
| LST_C      |             6 | BY       | Not Significant |    4267 |        85.34 |
| LST_C      |             8 | Raw      | High-High       |    1227 |        24.54 |
| LST_C      |             8 | Raw      | Low-Low         |    1260 |        25.2  |
| LST_C      |             8 | Raw      | High-Low        |      58 |         1.16 |
| LST_C      |             8 | Raw      | Low-High        |      72 |         1.44 |
| LST_C      |             8 | Raw      | Not Significant |    2383 |        47.66 |
| LST_C      |             8 | BH       | High-High       |    1066 |        21.32 |
| LST_C      |             8 | BH       | Low-Low         |     847 |        16.94 |
| LST_C      |             8 | BH       | High-Low        |      22 |         0.44 |
| LST_C      |             8 | BH       | Low-High        |      40 |         0.8  |
| LST_C      |             8 | BH       | Not Significant |    3025 |        60.5  |
| LST_C      |             8 | BY       | High-High       |     653 |        13.06 |
| LST_C      |             8 | BY       | Low-Low         |     421 |         8.42 |
| LST_C      |             8 | BY       | High-Low        |       4 |         0.08 |
| LST_C      |             8 | BY       | Low-High        |      14 |         0.28 |
| LST_C      |             8 | BY       | Not Significant |    3908 |        78.16 |
| LST_C      |            10 | Raw      | High-High       |    1289 |        25.78 |
| LST_C      |            10 | Raw      | Low-Low         |    1491 |        29.82 |
| LST_C      |            10 | Raw      | High-Low        |      75 |         1.5  |
| LST_C      |            10 | Raw      | Low-High        |      85 |         1.7  |
| LST_C      |            10 | Raw      | Not Significant |    2060 |        41.2  |
| LST_C      |            10 | BH       | High-High       |    1158 |        23.16 |
| LST_C      |            10 | BH       | Low-Low         |    1159 |        23.18 |
| LST_C      |            10 | BH       | High-Low        |      44 |         0.88 |
| LST_C      |            10 | BH       | Low-High        |      68 |         1.36 |
| LST_C      |            10 | BH       | Not Significant |    2571 |        51.42 |
| LST_C      |            10 | BY       | High-High       |     760 |        15.2  |
| LST_C      |            10 | BY       | Low-Low         |     549 |        10.98 |
| LST_C      |            10 | BY       | High-Low        |       7 |         0.14 |
| LST_C      |            10 | BY       | Low-High        |      12 |         0.24 |
| LST_C      |            10 | BY       | Not Significant |    3672 |        73.44 |

### Cluster stability

| Variable   | Comparison      |   Total_Samples |   Identical_Classification_Count |   Identical_Classification_Percentage |   Stable_Significant_Cluster_Count |   Stable_Significant_Cluster_Percentage |   Significant_Cluster_Jaccard |
|:-----------|:----------------|----------------:|---------------------------------:|--------------------------------------:|-----------------------------------:|----------------------------------------:|------------------------------:|
| NDVI       | K6_vs_K8_vs_K10 |            5000 |                             4279 |                                 85.58 |                                245 |                                    4.9  |                    nan        |
| NDVI       | K6_vs_K8        |            5000 |                             4663 |                                 93.26 |                                254 |                                    5.08 |                      0.42978  |
| NDVI       | K6_vs_K10       |            5000 |                             4322 |                                 86.44 |                                256 |                                    5.12 |                      0.27409  |
| NDVI       | K8_vs_K10       |            5000 |                             4573 |                                 91.46 |                                522 |                                   10.44 |                      0.550053 |
| NDBI       | K6_vs_K8_vs_K10 |            5000 |                             4473 |                                 89.46 |                                274 |                                    5.48 |                    nan        |
| NDBI       | K6_vs_K8        |            5000 |                             4740 |                                 94.8  |                                288 |                                    5.76 |                      0.525547 |
| NDBI       | K6_vs_K10       |            5000 |                             4528 |                                 90.56 |                                288 |                                    5.76 |                      0.378947 |
| NDBI       | K8_vs_K10       |            5000 |                             4678 |                                 93.56 |                                438 |                                    8.76 |                      0.576316 |
| LST_C      | K6_vs_K8_vs_K10 |            5000 |                             4093 |                                 81.86 |                               1573 |                                   31.46 |                    nan        |
| LST_C      | K6_vs_K8        |            5000 |                             4579 |                                 91.58 |                               1588 |                                   31.76 |                      0.790443 |
| LST_C      | K6_vs_K10       |            5000 |                             4139 |                                 82.78 |                               1595 |                                   31.9  |                      0.64943  |
| LST_C      | K8_vs_K10       |            5000 |                             4468 |                                 89.36 |                               1936 |                                   38.72 |                      0.784441 |

### Methodological considerations

- Spatial weights were independently constructed for K=6, 8 and 10.
- Global and local Moran statistics were evaluated using 4,999 permutations.
- The approximate minimum permutation p-value is 0.0002.
- BH and BY corrections were applied separately for each variable and K configuration.
- Cluster agreement and Jaccard overlap quantify different aspects of classification stability.
- Agreement in the Not Significant category does not represent agreement on a significant cluster.
- The stability analysis evaluates sensitivity to the selected KNN configuration, not independence of spatial tests.
- Spatial autocorrelation does not establish causal relationships.
- Results remain conditional on the spatial sampling design and selected study area.
