# 14_plot_continuous_maps.py
# خواندن فایل GeoTIFF و ساخت نقشه‌های پیوسته (Continuous) برای مقاله

import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# مسیر پوشه اصلی
BASE_DIR = r"E:\European universities\apply files\List of Apply\design portfolio\project\Tehran_Urban_Climate_Analysis"
TIF_PATH = os.path.join(BASE_DIR, "data", "rasters", "tehran_rasters_2024_summer.tif")
OUT_DIR = os.path.join(BASE_DIR, "figures", "gee")
os.makedirs(OUT_DIR, exist_ok=True)

def plot_map(data, title, cmap, vmin, vmax, out_name, cbar_label):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # ماسک کردن مقادیر خارج از محدوده (برای جلوگیری از سیاه شدن پس‌زمینه)
    masked_data = np.ma.masked_where((data < vmin) | (data > vmax) | np.isnan(data), data)
    
    im = ax.imshow(masked_data, cmap=cmap, vmin=vmin, vmax=vmax)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(cbar_label, fontsize=12)
    
    # ذخیره با کیفیت بالا
    out_path = os.path.join(OUT_DIR, out_name)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

print("Reading GeoTIFF...")
with rasterio.open(TIF_PATH) as src:
    print(f"Total bands found: {src.count}")
    
    # خواندن باندها (NDVI, NDBI, LST)
    ndvi = src.read(1)
    ndbi = src.read(2)
    lst = src.read(3)
    
    print("Generating NDVI Map...")
    plot_map(ndvi, "NDVI - Tehran (Summer 2024)", 
             'YlGn', -0.1, 0.6, "NDVI_continuous_2024.png", "NDVI")

    print("Generating NDBI Map...")
    plot_map(ndbi, "NDBI - Tehran (Summer 2024)", 
             'RdYlBu_r', -0.2, 0.2, "NDBI_continuous_2024.png", "NDBI")

    print("Generating LST Map...")
    lst_cmap = LinearSegmentedColormap.from_list("lst_cmap", 
        ["#313695", "#4575B4", "#FFFFBF", "#FDAE61", "#D73027"])
    
    plot_map(lst, "Land Surface Temperature (LST) - Tehran (Summer 2024)", 
             lst_cmap, 30, 55, "LST_continuous_2024.png", "LST (°C)")

print("All maps generated successfully!")