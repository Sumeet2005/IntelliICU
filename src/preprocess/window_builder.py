"""
Time Window Builder
Creates sliding windows of patient data for temporal modeling
"""

import pandas as pd
import numpy as np

class TimeWindowBuilder:
    """Build time windows for sequential prediction"""
    
    def __init__(self, window_size=6):
        self.window_size = window_size
    
    def create_windows(self, df, patient_id_col='Patient_ID'):
        """Create sliding windows for each patient"""
        windows = []
        labels = []
        patient_ids = []
        
        for patient_id in df[patient_id_col].unique():
            patient_df = df[df[patient_id_col] == patient_id].sort_values('Hour')
            
            if len(patient_df) < self.window_size:
                continue
            
            # Get feature columns
            feature_cols = [col for col in patient_df.columns 
                          if col not in ['Patient_ID', 'Hour', 'SepsisLabel', 'ICULOS']]
            
            # Create windows
            for i in range(len(patient_df) - self.window_size + 1):
                window = patient_df.iloc[i:i+self.window_size][feature_cols].values
                label = patient_df.iloc[i+self.window_size-1]['SepsisLabel']
                
                windows.append(window)
                labels.append(label)
                patient_ids.append(patient_id)
        
        return np.array(windows), np.array(labels), np.array(patient_ids)
    
    def create_single_window(self, patient_df):
        """Create window for single patient (for real-time prediction)"""
        feature_cols = [col for col in patient_df.columns 
                       if col not in ['Patient_ID', 'Hour', 'SepsisLabel', 'ICULOS']]
        
        if len(patient_df) < self.window_size:
            # Pad with zeros if not enough data
            padding = np.zeros((self.window_size - len(patient_df), len(feature_cols)))
            window = np.vstack([padding, patient_df[feature_cols].values])
        else:
            window = patient_df.tail(self.window_size)[feature_cols].values
        
        return window

# Usage
if __name__ == "__main__":
    df = pd.read_parquet('data/processed/sepsis_features_final.parquet')
    
    builder = TimeWindowBuilder(window_size=6)
    X_windows, y_windows, patient_ids = builder.create_windows(df)
    
    print(f"Created {len(X_windows)} windows")
    print(f"Window shape: {X_windows[0].shape}")
    
    # Save for LSTM/RNN models
    np.save('data/windows/X_windows.npy', X_windows)
    np.save('data/windows/y_windows.npy', y_windows)
