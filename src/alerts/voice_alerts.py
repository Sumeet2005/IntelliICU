"""
Voice Alert System
Announces alerts through computer speakers
"""

import pyttsx3

class VoiceAlerter:
    """Announce alerts via voice"""
    
    def __init__(self, config):
        self.config = config
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', config['rate'])
            self.engine.setProperty('volume', config['volume'])
            print("✅ Voice engine initialized")
        except Exception as e:
            print(f"⚠️ Voice not available: {e}")
            self.engine = None
    
    def announce_critical_alert(self, alert_data):
        """Announce critical alert"""
        if not self.engine:
            print("⚠️ Voice engine not available")
            return
        
        message = (
            f"Critical sepsis alert. "
            f"Patient number {alert_data['patient_id']}. "
            f"Risk score {alert_data['risk_score']:.0f} percent. "
            f"Immediate physician notification required. "
        )
        
        print(f"🔊 Voice Alert: {message}")
        self.engine.say(message)
        self.engine.runAndWait()
    
    def announce_high_alert(self, alert_data):
        """Announce high priority alert"""
        if not self.engine:
            return
        
        message = (
            f"High sepsis risk alert. "
            f"Patient number {alert_data['patient_id']}. "
            f"Risk score {alert_data['risk_score']:.0f} percent. "
        )
        
        print(f"🔊 Voice Alert: {message}")
        self.engine.say(message)
        self.engine.runAndWait()
