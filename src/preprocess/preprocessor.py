# src/preprocess/preprocessor.py

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class ICUPreprocessor:
    """
    Comprehensive preprocessing pipeline for PhysioNet Sepsis data
    """
    
    def __init__(self):
        self.scalers = {}
        self.feature_names = []
        
    def clean_outliers(self, df):
        """
        Remove physiologically impossible values and artifacts
        """
        print("\n" + "="*60)
        print("STEP 1: CLEANING OUTLIERS")
        print("="*60)
        
        # Define physiologically plausible ranges
        ranges = {
            'HR': (30, 200),
            'O2Sat': (50, 100),
            'Temp': (32, 42),
            'SBP': (50, 250),
            'MAP': (30, 200),
            'DBP': (20, 150),
            'Resp': (5, 60),
            'BaseExcess': (-30, 30),
            'HCO3': (5, 50),
            'FiO2': (0.21, 1.0),
            'pH': (6.8, 7.8),
            'PaCO2': (10, 100),
            'SaO2': (50, 100),
            'Glucose': (20, 600),
            'Lactate': (0, 20),
            'Creatinine': (0, 15),
            'BUN': (0, 200),
            'WBC': (0, 100),
            'Platelets': (0, 1000),
            'Age': (18, 100)
        }
        
        df_cleaned = df.copy()
        outliers_removed = {}
        
        for col, (low, high) in ranges.items():
            if col in df_cleaned.columns:
                original_count = df_cleaned[col].notna().sum()
                
                # Replace outliers with NaN
                df_cleaned.loc[(df_cleaned[col] < low) | (df_cleaned[col] > high), col] = np.nan
                
                new_count = df_cleaned[col].notna().sum()
                outliers_removed[col] = original_count - new_count
                
                if outliers_removed[col] > 0:
                    print(f"  {col:20s}: Removed {outliers_removed[col]:6d} outliers "
                          f"({outliers_removed[col]/original_count*100:5.2f}%)")
        
        total_outliers = sum(outliers_removed.values())
        print(f"\n✓ Total outliers removed: {total_outliers:,}")
        
        return df_cleaned
    
    def handle_missing_data(self, df, strategy='hybrid'):
        """
        Multi-strategy missing data imputation
        
        Strategy:
        - Forward fill vitals (persist 12h max)
        - Median fill rare labs (>90% missing)
        - Create missingness indicators for all
        """
        print("\n" + "="*60)
        print("STEP 2: HANDLING MISSING DATA")
        print("="*60)
        
        df_filled = df.copy()
        
        # Separate by patient to avoid cross-patient imputation
        if 'Patient_ID' in df.columns:
            patient_groups = df_filled.groupby('Patient_ID')
        else:
            print("⚠️ Warning: Patient_ID not found, imputing globally")
            patient_groups = [(0, df_filled)]
        
        # 1. Create missingness indicators FIRST
        print("\n1. Creating missingness indicators...")
        for col in df_filled.select_dtypes(include=[np.number]).columns:
            if col not in ['Patient_ID', 'Hour', 'ICULOS', 'SepsisLabel']:
                if df_filled[col].isnull().any():
                    df_filled[f'{col}_missing'] = df_filled[col].isnull().astype(int)
        
        # 2. Forward fill vitals (time-series continuity)
        vitals = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp']
        print("\n2. Forward filling vitals (limit: 12 hours)...")
        
        filled_dfs = []
        for patient_id, patient_df in patient_groups:
            patient_df = patient_df.sort_values('Hour') if 'Hour' in patient_df.columns else patient_df
            
            for vital in vitals:
                if vital in patient_df.columns:
                    patient_df[vital] = patient_df[vital].fillna(method='ffill', limit=12)
            
            filled_dfs.append(patient_df)
        
        df_filled = pd.concat(filled_dfs, ignore_index=True) if len(filled_dfs) > 1 else filled_dfs[0]
        
        # 3. Median fill rare labs (>90% missing)
        print("\n3. Median imputing rare labs...")
        rare_labs = df_filled.columns[df_filled.isnull().mean() > 0.9]
        numeric_rare_labs = [col for col in rare_labs if col in df_filled.select_dtypes(include=[np.number]).columns]
        
        for col in numeric_rare_labs:
            if col not in ['Patient_ID', 'SepsisLabel'] and not col.endswith('_missing'):
                median_val = df_filled[col].median()
                df_filled[col] = df_filled[col].fillna(median_val)
                print(f"  {col:25s}: Filled with median = {median_val:.2f}")
        
        # 4. Backward fill any remaining NaNs in vitals
        print("\n4. Backward filling remaining vital gaps...")
        for vital in vitals:
            if vital in df_filled.columns:
                df_filled[vital] = df_filled[vital].fillna(method='bfill', limit=6)
        
        # 5. Final median fill for any remaining NaNs
        numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
        remaining_missing = df_filled[numeric_cols].isnull().sum()
        remaining_missing = remaining_missing[remaining_missing > 0]
        
        if len(remaining_missing) > 0:
            print(f"\n5. Final median fill for {len(remaining_missing)} columns with remaining NaNs...")
            for col in remaining_missing.index:
                if col not in ['Patient_ID', 'SepsisLabel'] and not col.endswith('_missing'):
                    df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        
        # Report final missingness
        final_missing = df_filled.isnull().sum().sum()
        print(f"\n✓ Missing values remaining: {final_missing:,}")
        
        return df_filled
    
    def normalize_features(self, df, fit=True):
        """
        Z-score normalization for numeric features
        """
        print("\n" + "="*60)
        print("STEP 3: NORMALIZING FEATURES")
        print("="*60)
        
        df_normalized = df.copy()
        
        # Exclude these from normalization
        exclude_cols = ['Patient_ID', 'Hour', 'ICULOS', 'SepsisLabel', 
                       'Gender', 'Unit1', 'Unit2', 'HospAdmTime', 'Unnamed: 0']
        
        # Get numeric columns to normalize
        numeric_cols = df_normalized.select_dtypes(include=[np.number]).columns
        cols_to_normalize = [col for col in numeric_cols 
                            if col not in exclude_cols 
                            and not col.endswith('_missing')]
        
        print(f"Normalizing {len(cols_to_normalize)} features...")
        
        for col in cols_to_normalize:
            if fit:
                self.scalers[col] = StandardScaler()
                df_normalized[col] = self.scalers[col].fit_transform(df_normalized[[col]])
            else:
                if col in self.scalers:
                    df_normalized[col] = self.scalers[col].transform(df_normalized[[col]])
        
        print(f"✓ Normalization complete")
        
        return df_normalized
    
    def preprocess_full_pipeline(self, df, fit=True):
        """
        Run complete preprocessing pipeline
        """
        print("\n" + "="*70)
        print("STARTING FULL PREPROCESSING PIPELINE")
        print("="*70)
        print(f"Input shape: {df.shape}")
        
        # Step 1: Clean outliers
        df_cleaned = self.clean_outliers(df)
        
        # Step 2: Handle missing data
        df_filled = self.handle_missing_data(df_cleaned)
        
        # Step 3: Normalize
        df_normalized = self.normalize_features(df_filled, fit=fit)
        
        print("\n" + "="*70)
        print("✓ PREPROCESSING COMPLETE")
        print("="*70)
        print(f"Output shape: {df_normalized.shape}")
        print(f"Features added: {df_normalized.shape[1] - df.shape[1]} (missingness indicators)")
        
        return df_normalized


def preprocess_and_save():
    """
    Main function to preprocess data and save
    """
    from pathlib import Path
    
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # Load raw data
    print("Loading raw data...")
    input_path = PROJECT_ROOT / "data" / "processed" / "sepsis_cleaned.parquet"
    df = pd.read_parquet(input_path)
    
    print(f"Loaded {len(df):,} rows")
    
    # Initialize preprocessor
    preprocessor = ICUPreprocessor()
    
    # Run pipeline
    df_preprocessed = preprocessor.preprocess_full_pipeline(df, fit=True)
    
    # Save preprocessed data
    output_path = PROJECT_ROOT / "data" / "processed" / "sepsis_preprocessed.parquet"
    df_preprocessed.to_parquet(output_path, index=False, compression='gzip')
    
    print(f"\n✓ Saved to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Save preprocessor object for later use
    import joblib
    preprocessor_path = PROJECT_ROOT / "models" / "preprocessor.pkl"
    preprocessor_path.parent.mkdir(exist_ok=True)
    joblib.dump(preprocessor, preprocessor_path)
    print(f"✓ Saved preprocessor to: {preprocessor_path}")


if __name__ == "__main__":
    preprocess_and_save()
