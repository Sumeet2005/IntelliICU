"""
Feature Engineering Module
Creates temporal features, rolling statistics, and interaction features
"""

import pandas as pd
import numpy as np

class FeatureEngineer:
    """Create features for sepsis prediction"""
    
    def __init__(self):
        self.vital_signs = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp']
    
    def create_rolling_features(self, df, windows=[2, 4, 6]):
        """Create rolling mean and std for vital signs"""
        df_features = df.copy()
        
        for patient_id, patient_df in df.groupby('Patient_ID'):
            for col in self.vital_signs:
                if col in patient_df.columns:
                    for window in windows:
                        # Rolling mean
                        df_features.loc[patient_df.index, f'{col}_mean_{window}h'] = \
                            patient_df[col].rolling(window=window, min_periods=1).mean()
                        
                        # Rolling std
                        df_features.loc[patient_df.index, f'{col}_std_{window}h'] = \
                            patient_df[col].rolling(window=window, min_periods=1).std()
        
        return df_features
    
    def create_change_features(self, df):
        """Create change/delta features"""
        df_features = df.copy()
        
        for patient_id, patient_df in df.groupby('Patient_ID'):
            for col in self.vital_signs:
                if col in patient_df.columns:
                    # 1-hour change
                    df_features.loc[patient_df.index, f'{col}_change_1h'] = \
                        patient_df[col].diff()
                    
                    # % change
                    df_features.loc[patient_df.index, f'{col}_pct_change'] = \
                        patient_df[col].pct_change()
        
        return df_features
    
    def create_interaction_features(self, df):
        """Create interaction features"""
        df_features = df.copy()
        
        # Shock index: HR / SBP
        if 'HR' in df.columns and 'SBP' in df.columns:
            df_features['Shock_Index'] = df['HR'] / (df['SBP'] + 1)
        
        # Modified Early Warning Score components
        if 'Resp' in df.columns:
            df_features['Resp_abnormal'] = ((df['Resp'] < 9) | (df['Resp'] > 25)).astype(int)
        
        if 'O2Sat' in df.columns:
            df_features['O2Sat_low'] = (df['O2Sat'] < 92).astype(int)
        
        return df_features
    
    def create_trend_features(self, df):
        """Create trend features (increasing/decreasing)"""
        df_features = df.copy()
        
        for patient_id, patient_df in df.groupby('Patient_ID'):
            for col in self.vital_signs:
                if col in patient_df.columns:
                    # Trend: 1 if increasing, -1 if decreasing, 0 if stable
                    rolling_diff = patient_df[col].rolling(window=3, min_periods=1).apply(
                        lambda x: 1 if x.iloc[-1] > x.iloc[0] else (-1 if x.iloc[-1] < x.iloc[0] else 0)
                    )
                    df_features.loc[patient_df.index, f'{col}_trend'] = rolling_diff
        
        return df_features
    
    def engineer_features(self, df):
        """Run full feature engineering pipeline"""
        print("Starting feature engineering...")
        print(f"Initial features: {df.shape[1]}")
        
        df = self.create_rolling_features(df)
        print("Rolling features created")
        
        df = self.create_change_features(df)
        print("Change features created")
        
        df = self.create_interaction_features(df)
        print("Interaction features created")
        
        df = self.create_trend_features(df)
        print("Trend features created")
        
        print(f"Final features: {df.shape[1]}")
        return df

# Usage
if __name__ == "__main__":
    df = pd.read_parquet('data/processed/sepsis_cleaned.parquet')
    engineer = FeatureEngineer()
    df_features = engineer.engineer_features(df)
    df_features.to_parquet('data/processed/sepsis_features_final.parquet', index=False)
