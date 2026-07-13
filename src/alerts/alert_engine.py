"""
Alert System - Voice + SMS (No Email)
"""

import yaml
from datetime import datetime
from enum import Enum
from pathlib import Path

class AlertLevel(Enum):
    """Alert severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AlertEngine:
    """Manages Voice + SMS alerts"""
    
    def __init__(self, config_path='config/config.yaml'):
        """Load configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.alert_history = []
        
        # Initialize SMS alerts
        if self.config['alerts']['sms']['enabled']:
            from src.alerts.sms_alerts import SMSAlerter
            self.sms_alerter = SMSAlerter(self.config['alerts']['sms'])
        else:
            self.sms_alerter = None
        
        # Initialize voice alerts
        if self.config['alerts']['voice']['enabled']:
            from src.alerts.voice_alerts import VoiceAlerter
            self.voice_alerter = VoiceAlerter(self.config['alerts']['voice'])
        else:
            self.voice_alerter = None
    
    def evaluate_alert_level(self, risk_score, vitals):
        """Determine alert level based on risk score and vitals"""
        
        # Critical: Very high risk or critical vitals
        if risk_score > 75:
            return AlertLevel.CRITICAL
        
        if risk_score > 60:
            # Check for critical vital signs
            critical_vitals = (
                vitals.get('SBP', 100) < 90 or  # Hypotension
                vitals.get('SpO2', 95) < 88 or  # Severe hypoxemia
                vitals.get('HR', 80) > 130      # Severe tachycardia
            )
            if critical_vitals:
                return AlertLevel.CRITICAL
            return AlertLevel.HIGH
        
        if risk_score > 40:
            return AlertLevel.HIGH
        
        if risk_score > 20:
            return AlertLevel.MEDIUM
        
        return AlertLevel.LOW
    
    def send_alert(self, patient_id, risk_score, alert_level, vitals, explanation):
        """Send alert through Voice + SMS"""
        
        alert_data = {
            'alert_id': self._generate_alert_id(),
            'timestamp': datetime.now(),
            'patient_id': patient_id,
            'risk_score': risk_score,
            'level': alert_level.name,
            'vitals': vitals,
            'explanation': explanation
        }
        
        # Store in history
        self.alert_history.append(alert_data)
        
        # Send alerts based on severity
        if alert_level == AlertLevel.CRITICAL:
            self._send_critical_alert(alert_data)
        
        elif alert_level == AlertLevel.HIGH:
            self._send_high_alert(alert_data)
        
        elif alert_level == AlertLevel.MEDIUM:
            print(f"📊 MEDIUM ALERT for Patient #{patient_id}")
        
        return alert_data
    
    def _send_critical_alert(self, alert_data):
        """Send critical alert through ALL channels"""
        print(f"🚨 CRITICAL ALERT for Patient #{alert_data['patient_id']}")
        
        # Voice alert
        if self.voice_alerter:
            self.voice_alerter.announce_critical_alert(alert_data)
        
        # SMS alert
        if self.sms_alerter:
            recipients = self.config['alerts']['sms']['recipients']['critical']
            self.sms_alerter.send_critical_alert(alert_data, recipients)
    
    def _send_high_alert(self, alert_data):
        """Send high-priority alert"""
        print(f"⚠️ HIGH ALERT for Patient #{alert_data['patient_id']}")
        
        # Voice alert
        if self.voice_alerter:
            self.voice_alerter.announce_high_alert(alert_data)
        
        # SMS alert
        if self.sms_alerter:
            recipients = self.config['alerts']['sms']['recipients'].get('high', [])
            if recipients:
                self.sms_alerter.send_high_alert(alert_data, recipients)
    
    def _generate_alert_id(self):
        """Generate unique alert ID"""
        return f"ALT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def get_active_alerts(self):
        """Get all active alerts from last 24 hours"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=24)
        return [a for a in self.alert_history if a['timestamp'] > cutoff]
