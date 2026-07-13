"""
SHAP-based Explainer: Explains WHY patient is at risk
Shows which vital signs and factors are causing high risk
"""

import shap
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

class SepsisExplainer:
    """Provides human-readable explanations for sepsis predictions"""
    
    def __init__(self, model_path='models/xgboost_sepsis.pkl'):
        """Initialize explainer with trained model"""
        self.model = joblib.load(model_path)
        self.explainer = None
        self.feature_names = None
        
    def create_explainer(self, X_background):
        """Create SHAP explainer using background data"""
        print("Creating SHAP explainer... (this may take a minute)")
        self.explainer = shap.TreeExplainer(self.model)
        self.feature_names = X_background.columns.tolist()
        print("✅ Explainer ready!")
        
        # Save explainer
        joblib.dump(self.explainer, 'models/shap_explainer.pkl')
        
    def load_explainer(self):
        """Load pre-computed explainer"""
        try:
            self.explainer = joblib.load('models/shap_explainer.pkl')
            print("✅ Explainer loaded from disk")
        except FileNotFoundError:
            print("⚠️ No saved explainer found. Creating new one...")
            return False
        return True
    
    def explain_patient(self, X_patient, feature_names=None):
        """
        Get explanation for a single patient
        
        Args:
            X_patient: Patient features (1D array or DataFrame row)
            feature_names: List of feature names
            
        Returns:
            Dictionary with explanation details
        """
        if self.explainer is None:
            raise ValueError("Explainer not initialized. Run create_explainer() or load_explainer() first.")
        
        # Convert to proper format
        if isinstance(X_patient, pd.DataFrame):
            feature_names = X_patient.columns.tolist()
            X_patient = X_patient.values
        
        if len(X_patient.shape) == 1:
            X_patient = X_patient.reshape(1, -1)
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_patient)
        
        # Get base value (average prediction)
        base_value = self.explainer.expected_value
        
        # Get prediction
        prediction = self.model.predict_proba(X_patient)[0][1] * 100
        
        # Create explanation DataFrame
        explanation_df = pd.DataFrame({
            'Feature': feature_names,
            'Value': X_patient[0],
            'SHAP_Impact': shap_values[0],
            'Impact_Direction': ['↑ Increases Risk' if x > 0 else '↓ Decreases Risk' for x in shap_values[0]]
        })
        
        # Sort by absolute impact
        explanation_df['Abs_Impact'] = explanation_df['SHAP_Impact'].abs()
        explanation_df = explanation_df.sort_values('Abs_Impact', ascending=False)
        
        # Get top risk factors
        top_risk = explanation_df[explanation_df['SHAP_Impact'] > 0].head(5)
        top_protective = explanation_df[explanation_df['SHAP_Impact'] < 0].head(5)
        
        return {
            'prediction': prediction,
            'base_risk': base_value * 100,
            'explanation_df': explanation_df,
            'top_risk_factors': top_risk.to_dict('records'),
            'top_protective_factors': top_protective.to_dict('records'),
            'summary': self._generate_summary(top_risk, prediction)
        }
    
    def _generate_summary(self, top_risk, prediction):
        """Generate human-readable summary"""
        if prediction > 60:
            severity = "CRITICAL"
            emoji = "🔴"
        elif prediction > 40:
            severity = "HIGH"
            emoji = "🟡"
        else:
            severity = "MODERATE"
            emoji = "🟢"
        
        summary = f"{emoji} **{severity} RISK** ({prediction:.1f}%)\n\n"
        summary += "**Top Contributing Factors:**\n"
        
        for idx, row in top_risk.iterrows():
            feature = self._humanize_feature_name(row['Feature'])
            value = row['Value']
            impact = row['SHAP_Impact']
            
            summary += f"- **{feature}**: {value:.1f} (Impact: +{impact:.2f})\n"
        
        return summary
    
    def _humanize_feature_name(self, feature):
        """Convert technical feature names to readable names"""
        name_map = {
            'HR': 'Heart Rate',
            'O2Sat': 'Oxygen Saturation',
            'Temp': 'Temperature',
            'SBP': 'Systolic Blood Pressure',
            'MAP': 'Mean Arterial Pressure',
            'DBP': 'Diastolic Blood Pressure',
            'Resp': 'Respiratory Rate',
            'Lactate': 'Blood Lactate',
            'WBC': 'White Blood Cell Count',
            'Shock_Index': 'Shock Index'
        }
        
        # Handle compound feature names (e.g., "HR_mean_4h")
        for key, value in name_map.items():
            if key in feature:
                return feature.replace(key, value)
        
        return feature.replace('_', ' ').title()
