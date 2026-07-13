"""
Data Resampling Module
Handles class imbalance for sepsis prediction
"""

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek
import pandas as pd
import numpy as np

class DataResampler:
    """Handle class imbalance in sepsis data"""
    
    def __init__(self, method='smote'):
        self.method = method
    
    def resample(self, X, y):
        """Apply resampling technique"""
        print(f"Original class distribution:\n{pd.Series(y).value_counts()}")
        
        if self.method == 'smote':
            sampler = SMOTE(random_state=42)
        elif self.method == 'undersample':
            sampler = RandomUnderSampler(random_state=42)
        elif self.method == 'smotetomek':
            sampler = SMOTETomek(random_state=42)
        else:
            return X, y
        
        X_resampled, y_resampled = sampler.fit_resample(X, y)
        
        print(f"Resampled class distribution:\n{pd.Series(y_resampled).value_counts()}")
        
        return X_resampled, y_resampled

# Usage
if __name__ == "__main__":
    from sklearn.model_selection import train_test_split
    
    df = pd.read_parquet('data/processed/sepsis_features_final.parquet')
    
    X = df.drop(['SepsisLabel', 'Patient_ID', 'Hour'], axis=1)
    y = df['SepsisLabel']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    resampler = DataResampler(method='smote')
    X_train_resampled, y_train_resampled = resampler.resample(X_train, y_train)
