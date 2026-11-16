# 15_HPI_calculation.py
# محاسبه شاخص HPI بر اساس نقاط نمونه و همچنین نقشه پیوسته (Raster)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import rasterio

BASE_DIR = r"E:\European universities\apply files\List of Apply\design portfolio\project\Tehran_Urban_Climate_Analysis"
CSV_PATH = os.path.join(BASE_DIR, "data", "samples", "tehran_stage06_sample_2024.csv")
TIF_PATH = os.path.join(BASE_DIR, "data", "rasters", "tehran_rasters_2024_summer.tif")
OUT_DIR = os.path.join(BASE_DIR, "figures", "gee")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# ==========================================
# بخش ۱: تحلیل آماری روی ۵۰۰۰ نقطه (CSV)
# ==========================================
print("--- PART 1: Point-based HPI (CSV) ---")
df = pd.read_csv(CSV_PATH)
df['LST_norm'] = normalize(df['LST_C'])
df['NDVI_norm'] = normalize(df['NDVI'])
df['HPI'] = df['LST_norm'] * (1 - df['NDVI_norm'])

out_csv = os.path.join(RESULTS_DIR, "hpi_sample_results.csv")
df.to_csv(out_csv, index=False)

print("\n--- TOP 5 HIGHEST PRIORITY LOCATIONS (CSV) ---")
top_5 = df.nlargest(5, 'HPI')[['lon', 'lat', 'LST_C', 'NDVI', 'HPI']]
print(top_5.to_string(index=False))

# ==========================================
# بخش ۲: نقشه پیوسته (Raster) از GeoTIFF
# ==========================================
print("\n--- PART 2: Continuous HPI (Raster) ---")
with rasterio.open(TIF_PATH) as src:
    ndvi = src.read(1)
    lst = src.read(3)
    
    # ماسک کردن مقادیر منفی یا NoData
    valid_mask = (ndvi > -1) & (lst > 0) & (~np.isnan(ndvi)) & (~np.isnan(lst))
    
    # نرمال‌سازی پیوسته (بین 0 و 1) بر اساس مقادیر معتبر
    lst_min, lst_max = np.min(lst[valid_mask]), np.max(lst[valid_mask])
    ndvi_min, ndvi_max = np.min(ndvi[valid_mask]), np.max(ndvi[valid_mask])
    
    lst_norm = (lst - lst_min) / (lst_max - lst_min)
    ndvi_norm = (ndvi - ndvi_min) / (ndvi_max - ndvi_min)
    
    # محاسبه HPI پیوسته
    hpi_raster = lst_norm * (1 - ndvi_norm)
    hpi_raster[~valid_mask] = np.nan

    # 1. رسم نقشه پیوسته (Continuous)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(hpi_raster, cmap='magma')
    ax.set_title("Continuous HPI - Tehran (Summer 2024)", fontsize=14, fontweight='bold')
    ax.set_xticks([]); ax.set_yticks([])
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("HPI (Higher = Higher Priority)")
    plt.savefig(os.path.join(OUT_DIR, "HPI_raster_continuous.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. رسم نقشه طبقه‌بندی شده (Categorized)
    # تقسیم به ۵ کلاس از اولویت خیلی کم تا خیلی زیاد
    fig, ax = plt.subplots(figsize=(10, 8))
    categories = np.zeros_like(hpi_raster)
    categories[(hpi_raster >= 0) & (hpi_raster < 0.2)] = 1 # خیلی کم
    categories[(hpi_raster >= 0.2) & (hpi_raster < 0.4)] = 2 # کم
    categories[(hpi_raster >= 0.4) & (hpi_raster < 0.6)] = 3 # متوسط
    categories[(hpi_raster >= 0.6) & (hpi_raster < 0.8)] = 4 # زیاد
    categories[(hpi_raster >= 0.8)] = 5 # خیلی زیاد (اولویت فوری)
    categories[~valid_mask] = np.nan

    from matplotlib.colors import ListedColormap
    cmap_cat = ListedColormap(['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c'])
    
    im2 = ax.imshow(categories, cmap=cmap_cat, vmin=1, vmax=5)
    ax.set_title("Categorized HPI Priority Zones - Tehran (Summer 2024)", fontsize=14, fontweight='bold')
    ax.set_xticks([]); ax.set_yticks([])
    
    cbar2 = plt.colorbar(im2, ax=ax, fraction=0.046, pad=0.04, ticks=[1.4, 2.2, 3.0, 3.8, 4.6])
    cbar2.ax.set_yticklabels(['Very Low', 'Low', 'Moderate', 'High', 'Very High (Urgent)'])
    cbar2.set_label("Priority Level")
    
    plt.savefig(os.path.join(OUT_DIR, "HPI_raster_categorized.png"), dpi=300, bbox_inches='tight')
    plt.close()

print("\nAll HPI maps (Continuous & Categorized) saved successfully!")