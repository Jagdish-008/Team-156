import json
import logging
import os

class DiagnosisEngine:
    def __init__(self):
        self.symptoms_rules = self.load_symptoms_rules()
        self.hospitals_data = self.load_hospitals_data()
    
    def load_symptoms_rules(self):
        """Load symptom-diagnosis rules from JSON file"""
        try:
            with open('data/symptoms_rules.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading symptoms rules: {str(e)}")
            return self.get_default_symptoms_rules()
    
    def load_hospitals_data(self):
        """Load hospitals data from JSON file"""
        try:
            with open('data/hospitals.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading hospitals data: {str(e)}")
            return self.get_default_hospitals_data()
    
    def get_default_symptoms_rules(self):
        """Default symptom-diagnosis rules if file not found"""
        return {
            "conditions": {
                "common_cold": {
                    "name_en": "Common Cold",
                    "name_hi": "सामान्य सर्दी",
                    "symptoms": ["cough", "runny nose", "sneezing", "sore throat", "mild fever"],
                    "keywords": ["cough", "cold", "runny", "nose", "sneeze", "throat", "खांसी", "सर्दी", "नाक"],
                    "advice_en": "Rest, drink fluids, use warm salt water for gargling. See a doctor if symptoms persist for more than 7 days.",
                    "advice_hi": "आराम करें, तरल पदार्थ पिएं, गर्म नमक के पानी से गरारे करें। यदि लक्षण 7 दिन से अधिक बने रहें तो डॉक्टर से मिलें।",
                    "severity": "mild"
                },
                "fever": {
                    "name_en": "Fever",
                    "name_hi": "बुखार",
                    "symptoms": ["high temperature", "chills", "sweating", "headache", "body ache"],
                    "keywords": ["fever", "temperature", "hot", "chills", "sweating", "बुखार", "तापमान", "ठंड"],
                    "advice_en": "Rest, drink plenty of fluids, take paracetamol. Seek immediate medical attention if fever is above 104°F (40°C).",
                    "advice_hi": "आराम करें, पर्याप्त तरल पदार्थ पिएं, पैरासिटामोल लें। यदि बुखार 104°F (40°C) से अधिक है तो तुरंत चिकित्सा सहायता लें।",
                    "severity": "moderate"
                },
                "headache": {
                    "name_en": "Headache",
                    "name_hi": "सिरदर्द",
                    "symptoms": ["head pain", "pressure", "throbbing", "sensitivity to light"],
                    "keywords": ["headache", "head", "pain", "migraine", "pressure", "सिरदर्द", "सिर", "दर्द"],
                    "advice_en": "Rest in a quiet, dark room. Apply cold or warm compress. Stay hydrated. Consult a doctor if severe or persistent.",
                    "advice_hi": "शांत, अंधेरे कमरे में आराम करें। ठंडी या गर्म सिकाई करें। पानी पिएं। यदि गंभीर या लगातार हो तो डॉक्टर से सलाह लें।",
                    "severity": "mild"
                },
                "stomach_pain": {
                    "name_en": "Stomach Pain",
                    "name_hi": "पेट दर्द",
                    "symptoms": ["abdominal pain", "cramping", "nausea", "bloating"],
                    "keywords": ["stomach", "belly", "abdominal", "pain", "cramp", "nausea", "पेट", "दर्द", "मतली"],
                    "advice_en": "Avoid solid foods temporarily. Drink clear fluids. Apply heat pad. See a doctor if severe pain or vomiting persists.",
                    "advice_hi": "अस्थायी रूप से ठोस भोजन से बचें। साफ तरल पदार्थ पिएं। गर्म पैड लगाएं। यदि तेज दर्द या उल्टी जारी रहे तो डॉक्टर से मिलें।",
                    "severity": "moderate"
                },
                "diarrhea": {
                    "name_en": "Diarrhea",
                    "name_hi": "दस्त",
                    "symptoms": ["loose stools", "frequent bowel movements", "dehydration"],
                    "keywords": ["diarrhea", "loose", "stool", "bathroom", "frequent", "दस्त", "पेट", "खराब"],
                    "advice_en": "Stay hydrated with ORS solution. Eat bland foods like rice, banana. Avoid dairy. See doctor if blood in stool or severe dehydration.",
                    "advice_hi": "ORS घोल से हाइड्रेटेड रहें। चावल, केला जैसे सादे भोजन खाएं। डेयरी से बचें। यदि मल में खून या गंभीर निर्जलीकरण हो तो डॉक्टर से मिलें।",
                    "severity": "moderate"
                }
            }
        }
    
    def get_default_hospitals_data(self):
        """Default hospitals data if file not found"""
        return {
            "hospitals": [
                {
                    "name": "AIIMS Delhi",
                    "city": "Delhi",
                    "state": "Delhi",
                    "phone": "+91-11-26588500",
                    "emergency": "+91-11-26588663",
                    "type": "Government",
                    "specialties": ["General Medicine", "Emergency", "Pediatrics", "Surgery"]
                },
                {
                    "name": "King George's Medical University",
                    "city": "Lucknow",
                    "state": "Uttar Pradesh",
                    "phone": "+91-522-2257540",
                    "emergency": "+91-522-2257450",
                    "type": "Government",
                    "specialties": ["General Medicine", "Emergency", "Cardiology"]
                },
                {
                    "name": "Seth GS Medical College and KEM Hospital",
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "phone": "+91-22-24129884",
                    "emergency": "+91-22-24138888",
                    "type": "Government",
                    "specialties": ["General Medicine", "Emergency", "Surgery"]
                },
                {
                    "name": "Government Medical College",
                    "city": "Chandigarh",
                    "state": "Chandigarh",
                    "phone": "+91-172-2601023",
                    "emergency": "+91-172-2601056",
                    "type": "Government",
                    "specialties": ["General Medicine", "Emergency", "Pediatrics"]
                },
                {
                    "name": "Rajendra Institute of Medical Sciences",
                    "city": "Ranchi",
                    "state": "Jharkhand",
                    "phone": "+91-651-2451070",
                    "emergency": "+91-651-2451080",
                    "type": "Government",
                    "specialties": ["General Medicine", "Emergency", "Surgery"]
                }
            ]
        }
    
    def analyze_symptoms(self, symptoms, age, severity, duration):
        """Analyze symptoms and return possible diagnosis"""
        try:
            possible_conditions = []
            symptoms_text = ' '.join(symptoms).lower()
            
            for condition_id, condition_data in self.symptoms_rules['conditions'].items():
                match_score = 0
                for keyword in condition_data['keywords']:
                    if keyword.lower() in symptoms_text:
                        match_score += 1
                
                if match_score > 0:
                    possible_conditions.append({
                        'id': condition_id,
                        'name_en': condition_data['name_en'],
                        'name_hi': condition_data['name_hi'],
                        'advice_en': condition_data['advice_en'],
                        'advice_hi': condition_data['advice_hi'],
                        'severity': condition_data['severity'],
                        'match_score': match_score
                    })
            
            # Sort by match score
            possible_conditions.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Determine urgency based on age, severity, and symptoms
            urgency = self.determine_urgency(age, severity, symptoms_text)
            
            return {
                'conditions': possible_conditions[:3],  # Return top 3 matches
                'urgency': urgency,
                'disclaimer': True
            }
            
        except Exception as e:
            logging.error(f"Error analyzing symptoms: {str(e)}")
            return {
                'conditions': [],
                'urgency': 'moderate',
                'disclaimer': True,
                'error': 'Unable to analyze symptoms'
            }
    
    def determine_urgency(self, age, severity, symptoms_text):
        """Determine urgency level based on various factors"""
        try:
            high_risk_symptoms = [
                'chest pain', 'difficulty breathing', 'severe pain', 'bleeding',
                'unconscious', 'seizure', 'high fever', 'severe headache'
            ]
            
            # Check for high-risk symptoms
            if any(symptom in symptoms_text for symptom in high_risk_symptoms):
                return 'high'
            
            # Age-based risk
            if age < 5 or age > 65:
                if severity == 'severe':
                    return 'high'
                elif severity == 'moderate':
                    return 'moderate'
            
            # Severity-based urgency
            if severity == 'severe':
                return 'high'
            elif severity == 'moderate':
                return 'moderate'
            else:
                return 'low'
                
        except Exception as e:
            logging.error(f"Error determining urgency: {str(e)}")
            return 'moderate'
    
    def get_nearby_hospitals(self, location):
        """Get hospitals near the specified location"""
        try:
            location_lower = location.lower()
            matching_hospitals = []
            
            for hospital in self.hospitals_data['hospitals']:
                # Simple matching based on city or state
                if (location_lower in hospital['city'].lower() or 
                    location_lower in hospital['state'].lower() or
                    hospital['city'].lower() in location_lower or
                    hospital['state'].lower() in location_lower):
                    matching_hospitals.append(hospital)
            
            # If no exact matches, return a few general hospitals
            if not matching_hospitals:
                matching_hospitals = self.hospitals_data['hospitals'][:3]
            
            return matching_hospitals[:5]  # Return max 5 hospitals
            
        except Exception as e:
            logging.error(f"Error getting nearby hospitals: {str(e)}")
            return []
