"""
Treatment Recommendation Engine
Provides evidence-based clinical recommendations
"""

class TreatmentEngine:
    """Generate treatment recommendations based on risk and vitals"""
    
    def __init__(self):
        self.sepsis_bundle = {
            'critical': [
                "🩸 Draw blood cultures (2 sets from different sites) BEFORE antibiotics",
                "💉 Start broad-spectrum antibiotics within 1 hour",
                "💧 Administer IV crystalloid bolus (30 mL/kg over 3 hours)",
                "🧪 Measure serum lactate immediately",
                "📊 Monitor vital signs every 15 minutes",
                "🏥 Consider ICU transfer if not already in ICU",
                "💊 Prepare vasopressors if MAP <65 mmHg after fluid resuscitation",
                "🫁 Supplemental oxygen to maintain SpO2 >92%"
            ],
            'high': [
                "👨‍⚕️ Alert attending physician within 30 minutes",
                "📈 Increase vital signs monitoring to every 30 minutes",
                "🧪 Order serum lactate within 2 hours",
                "🩺 Perform thorough physical exam and reassess",
                "🔬 Review recent laboratory results and trends",
                "🦠 Assess and document potential infection sources",
                "📝 Document all clinical changes in patient chart",
                "💧 Consider preventive IV fluid hydration"
            ],
            'medium': [
                "👀 Monitor vital signs every hour",
                "📋 Continue routine ICU protocols",
                "🔔 Notify charge nurse of elevated risk status",
                "📝 Document patient status and trends",
                "🩺 Reassess if condition changes"
            ],
            'low': [
                "✅ Continue standard ICU monitoring",
                "📊 Routine vital signs assessment",
                "📝 Document stable status"
            ]
        }
    
    def get_recommendations(self, risk_score, vitals, explanation=None):
        """Get personalized treatment recommendations"""
        
        # Determine risk level
        if risk_score > 60:
            level = 'critical'
        elif risk_score > 40:
            level = 'high'
        elif risk_score > 20:
            level = 'medium'
        else:
            level = 'low'
        
        recommendations = self.sepsis_bundle[level].copy()
        
        # Add vital-sign specific recommendations
        specific_recs = self._get_vital_specific_recommendations(vitals)
        recommendations.extend(specific_recs)
        
        return {
            'level': level,
            'recommendations': recommendations,
            'rationale': self._get_rationale(level, risk_score, vitals)
        }
    
    def _get_vital_specific_recommendations(self, vitals):
        """Generate recommendations based on specific vital signs"""
        recs = []
        
        # Hypotension
        if vitals.get('SBP', 120) < 90:
            recs.append("🩸 HYPOTENSION: Fluid resuscitation priority, consider vasopressors")
        
        # Hypoxemia
        if vitals.get('SpO2', 95) < 92:
            recs.append("🫁 HYPOXEMIA: Increase oxygen support, consider non-rebreather mask")
        
        # Tachycardia
        if vitals.get('HR', 80) > 110:
            recs.append("❤️ TACHYCARDIA: Assess for hypovolemia, pain, or anxiety")
        
        # Fever
        if vitals.get('Temp', 37) > 38.5:
            recs.append("🌡️ FEVER: Consider antipyretics, cooling measures, blood cultures")
        
        # Elevated lactate
        if vitals.get('Lactate', 2) > 2.0:
            recs.append("🧪 ELEVATED LACTATE: Aggressive fluid resuscitation, recheck in 2-4 hours")
        
        # Tachypnea
        if vitals.get('RR', 16) > 22:
            recs.append("💨 TACHYPNEA: Assess for respiratory distress, consider ABG")
        
        return recs
    
    def _get_rationale(self, level, risk_score, vitals):
        """Explain the reasoning behind recommendations"""
        if level == 'critical':
            return (
                f"Patient has {risk_score:.1f}% sepsis risk with concerning vital signs. "
                "Early recognition and aggressive management within the first hour "
                "(the 'golden hour') significantly improves survival rates. "
                "Sepsis-3 criteria and surviving sepsis campaign guidelines recommend "
                "immediate initiation of sepsis bundle."
            )
        elif level == 'high':
            return (
                f"Patient shows {risk_score:.1f}% sepsis risk. "
                "Enhanced surveillance and early intervention can prevent progression "
                "to severe sepsis or septic shock."
            )
        elif level == 'medium':
            return (
                f"Patient has {risk_score:.1f}% risk. "
                "Continued monitoring recommended to detect early deterioration."
            )
        else:
            return "Patient currently stable. Continue routine monitoring."
    
    def get_antibiotic_recommendations(self, infection_source='unknown'):
        """Recommend antibiotics based on suspected infection source"""
        antibiotic_guide = {
            'pneumonia': [
                "Ceftriaxone 1-2g IV q24h PLUS",
                "Azithromycin 500mg IV q24h"
            ],
            'urinary': [
                "Ceftriaxone 1-2g IV q24h"
            ],
            'abdominal': [
                "Piperacillin-Tazobactam 4.5g IV q6h"
            ],
            'skin': [
                "Vancomycin 15-20mg/kg IV q12h PLUS",
                "Piperacillin-Tazobactam 4.5g IV q6h"
            ],
            'unknown': [
                "Vancomycin 15-20mg/kg IV q12h PLUS",
                "Piperacillin-Tazobactam 4.5g IV q6h",
                "(Broad-spectrum coverage for unknown source)"
            ]
        }
        
        return antibiotic_guide.get(infection_source, antibiotic_guide['unknown'])
