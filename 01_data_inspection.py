
import os
import glob
import pandas as pd
import numpy as np

# Project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directory
RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")

print("=" * 60)
print("TEHRAN URBAN CLIMATE ANALYSIS")
print("STAGE 01: DATA INSPECTION")
print("=" * 60)

# Find CSV files
csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

print("\nCSV FILES FOUND:", len(csv_files))

if not csv_files:
    print("No CSV files found in data/raw folder.")

for file in csv_files:

    print("\n" + "=" * 50)
    print("FILE:", os.path.basename(file))
    print("=" * 50)

    df = pd.read_csv(file)

    print("\nDATASET SHAPE:")
    print(df.shape)

    print("\nCOLUMN NAMES:")
    print(df.columns.tolist())

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\nFIRST 5 ROWS:")
    print(df.head())

    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    print("\nSTATISTICAL SUMMARY:")
    print(df.describe())

print("\nINSPECTION COMPLETED!")
