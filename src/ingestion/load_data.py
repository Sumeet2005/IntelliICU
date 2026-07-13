# src/ingestion/load_data.py

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_PATH = PROJECT_ROOT / "data" / "raw" / "physionet_sepsis.csv"

def load_data(path=DEFAULT_PATH, nrows=None):
    """
    Load PhysioNet Sepsis 2019 dataset from Kaggle format
    
    Args:
        path: Path to physionet_sepsis.csv file
        nrows: Number of rows to load (None = all rows)
    
    Returns:
        df: Pandas DataFrame with all patient time-series data
    """
    print(f"Loading data from: {path}")
    
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at {path}\n"
            f"Please download from Kaggle and place in data/raw/"
        )
    
    # Load the CSV
    df = pd.read_csv(path, nrows=nrows)
    
    print(f"✓ Loaded {len(df):,} rows")
    print(f"✓ Shape: {df.shape}")
    print(f"✓ Columns: {len(df.columns)}")
    
    # Display basic info
    print("\n" + "="*60)
    print("DATASET OVERVIEW")
    print("="*60)
    
    # Column names
    print("\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Data types
    print(f"\nData Types:")
    print(df.dtypes.value_counts())
    
    # Missing data summary
    print(f"\nMissing Data (Top 15):")
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    print(missing_pct.head(15))
    
    # Basic statistics for key vitals
    print(f"\n" + "="*60)
    print("KEY VITAL SIGNS STATISTICS")
    print("="*60)
    
    vital_cols = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'Resp']
    available_vitals = [col for col in vital_cols if col in df.columns]
    
    if available_vitals:
        print(df[available_vitals].describe())
    
    # Check for target column
    if 'SepsisLabel' in df.columns:
        sepsis_rate = df['SepsisLabel'].mean() * 100
        print(f"\n✓ SepsisLabel found")
        print(f"  Sepsis positive rate: {sepsis_rate:.2f}%")
        print(f"  Positive samples: {df['SepsisLabel'].sum():,}")
        print(f"  Negative samples: {(df['SepsisLabel']==0).sum():,}")
    
    # Patient count (if Patient ID column exists)
    patient_cols = ['Patient', 'patient_id', 'PatientID']
    for col in patient_cols:
        if col in df.columns:
            n_patients = df[col].nunique()
            print(f"\n✓ Total unique patients: {n_patients:,}")
            print(f"  Average hours per patient: {len(df)/n_patients:.1f}")
            break
    
    return df


def quick_explore(df):
    """
    Quick data exploration for PhysioNet Sepsis dataset
    """
    print("\n" + "="*60)
    print("QUICK EXPLORATION")
    print("="*60)
    
    # Sample rows
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Check for outliers in vitals
    print("\n" + "="*60)
    print("POTENTIAL OUTLIERS DETECTED")
    print("="*60)
    
    outlier_checks = {
        'HR': (30, 200),
        'O2Sat': (50, 100),
        'Temp': (32, 42),
        'SBP': (50, 250),
        'MAP': (30, 200),
        'Resp': (5, 60)
    }
    
    for col, (low, high) in outlier_checks.items():
        if col in df.columns:
            outliers = df[(df[col] < low) | (df[col] > high)][col].dropna()
            if len(outliers) > 0:
                print(f"\n{col}:")
                print(f"  Values outside [{low}, {high}]: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")
                print(f"  Min: {df[col].min():.1f}, Max: {df[col].max():.1f}")


def save_processed(df, output_path=None):
    """
    Save cleaned data to processed folder
    """
    if output_path is None:
        output_path = PROJECT_ROOT / "data" / "processed" / "sepsis_cleaned.parquet"
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet (compressed, faster than CSV)
    df.to_parquet(output_path, index=False, compression='gzip')
    print(f"\n✓ Saved to: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")


# Run when file is executed directly
if __name__ == "__main__":
    print("\n" + "="*60)
    print("SMART ICU AI - DATA INGESTION MODULE")
    print("="*60 + "\n")
    
    # Load full dataset (or use nrows=10000 for testing)
    df = load_data(nrows=50000)  # Start with 50k rows for testing
    
    # Quick exploration
    quick_explore(df)
    
    # Save to processed folder
    save_processed(df)
    
    print("\n" + "="*60)
    print("✓ DATA INGESTION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review the missing data percentages")
    print("  2. Check for outliers in vital signs")
    print("  3. Run full load with load_data() if 50k sample looks good")
    print("  4. Proceed to preprocessing pipeline")
