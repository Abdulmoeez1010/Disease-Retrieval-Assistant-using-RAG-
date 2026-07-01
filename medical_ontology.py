"""
Medical Knowledge Ontology
Represents diseases, symptoms, treatments, and their relationships
"""

class MedicalOntology:
    def __init__(self):
        self.ontology = {
            # ========== DISEASES ==========
            "diseases": {
                "dengue_fever": {
                    "name": "Dengue Fever",
                    "type": "viral_infection",
                    "symptoms": [
                        "high_fever", "severe_headache", "pain_behind_eyes",
                        "joint_pain", "muscle_pain", "skin_rash", "nausea",
                        "vomiting", "mild_bleeding"
                    ],
                    "severity": "moderate_to_severe",
                    "requires_immediate_care": True,
                    "caused_by": ["dengue_virus"],
                    "transmitted_by": ["aedes_mosquito"],
                    "treatments": ["rest", "hydration", "pain_relievers", "monitoring"],
                    "complications": ["dengue_hemorrhagic_fever", "dengue_shock_syndrome"],
                    "prevention": ["mosquito_control", "protective_clothing", "repellent"],
                    "diagnosis_methods": ["blood_test", "ns1_antigen_test"]
                },
                
                "malaria": {
                    "name": "Malaria",
                    "type": "parasitic_infection",
                    "symptoms": [
                        "high_fever", "chills", "sweating", "headache",
                        "nausea", "vomiting", "muscle_pain", "fatigue"
                    ],
                    "severity": "moderate_to_severe",
                    "requires_immediate_care": True,
                    "caused_by": ["plasmodium_parasite"],
                    "transmitted_by": ["anopheles_mosquito"],
                    "treatments": ["antimalarial_drugs", "chloroquine", "artemisinin"],
                    "complications": ["cerebral_malaria", "organ_failure"],
                    "prevention": ["mosquito_nets", "antimalarial_prophylaxis"],
                    "diagnosis_methods": ["blood_smear", "rapid_diagnostic_test"]
                },
                
                "common_cold": {
                    "name": "Common Cold",
                    "type": "viral_infection",
                    "symptoms": [
                        "runny_nose", "sneezing", "sore_throat", "cough",
                        "mild_headache", "mild_fever", "fatigue"
                    ],
                    "severity": "mild",
                    "requires_immediate_care": False,
                    "caused_by": ["rhinovirus", "coronavirus"],
                    "transmitted_by": ["airborne_droplets", "contact"],
                    "treatments": ["rest", "hydration", "over_the_counter_meds"],
                    "complications": ["sinusitis", "ear_infection"],
                    "prevention": ["hand_washing", "avoid_contact"],
                    "diagnosis_methods": ["clinical_examination"]
                },
                
                "migraine": {
                    "name": "Migraine",
                    "type": "neurological_condition",
                    "symptoms": [
                        "severe_headache", "nausea", "vomiting",
                        "sensitivity_to_light", "sensitivity_to_sound", "visual_aura"
                    ],
                    "severity": "moderate_to_severe",
                    "requires_immediate_care": False,
                    "caused_by": ["genetic_factors", "hormonal_changes", "stress"],
                    "treatments": ["pain_relievers", "triptans", "rest_in_dark_room"],
                    "triggers": ["stress", "lack_of_sleep", "certain_foods", "bright_lights"],
                    "prevention": ["avoid_triggers", "regular_sleep", "stress_management"],
                    "diagnosis_methods": ["clinical_history", "neurological_exam"]
                }
            },
            
            # ========== SYMPTOMS ==========
            "symptoms": {
                "high_fever": {
                    "name": "High Fever",
                    "severity_indicator": True,
                    "related_diseases": ["dengue_fever", "malaria", "flu"],
                    "body_part": "systemic",
                    "urgent_if": ["above_103F", "lasts_more_than_3_days"]
                },
                
                "severe_headache": {
                    "name": "Severe Headache",
                    "severity_indicator": True,
                    "related_diseases": ["dengue_fever", "malaria", "migraine", "meningitis"],
                    "body_part": "head",
                    "urgent_if": ["sudden_onset", "worst_ever", "with_stiff_neck"]
                },
                
                "skin_rash": {
                    "name": "Skin Rash",
                    "severity_indicator": False,
                    "related_diseases": ["dengue_fever", "measles", "allergic_reaction"],
                    "body_part": "skin",
                    "urgent_if": ["with_fever", "spreading_rapidly", "with_breathing_difficulty"]
                },
                
                "joint_pain": {
                    "name": "Joint Pain",
                    "severity_indicator": False,
                    "related_diseases": ["dengue_fever", "chikungunya", "arthritis"],
                    "body_part": "joints",
                    "urgent_if": ["severe_swelling", "unable_to_move"]
                }
            },
            
            # ========== REASONING RULES ==========
            "rules": [
                {
                    "name": "Dengue Detection Rule",
                    "condition": {
                        "all_of": ["high_fever", "severe_headache"],
                        "any_of": ["skin_rash", "pain_behind_eyes", "joint_pain"]
                    },
                    "conclusion": "dengue_fever",
                    "confidence": 0.8
                },
                
                {
                    "name": "Malaria Detection Rule",
                    "condition": {
                        "all_of": ["high_fever", "chills"],
                        "any_of": ["sweating", "headache"]
                    },
                    "conclusion": "malaria",
                    "confidence": 0.75
                },
                
                {
                    "name": "Emergency Rule",
                    "condition": {
                        "any_of": ["high_fever", "severe_headache", "difficulty_breathing"],
                        "duration": "more_than_3_days"
                    },
                    "conclusion": "seek_immediate_medical_attention",
                    "confidence": 1.0
                }
            ],
            
            # ========== BODY PARTS ==========
            "body_parts": {
                "head": ["brain", "eyes", "ears", "nose", "mouth"],
                "chest": ["lungs", "heart"],
                "abdomen": ["stomach", "liver", "intestines"],
                "limbs": ["arms", "legs", "hands", "feet"]
            }
        }
    
    def get_disease_info(self, disease_id):
        """Get information about a specific disease"""
        return self.ontology["diseases"].get(disease_id)
    
    def get_symptom_info(self, symptom_id):
        """Get information about a specific symptom"""
        return self.ontology["symptoms"].get(symptom_id)
    
    def get_diseases_by_symptom(self, symptom):
        """Find all diseases associated with a symptom"""
        diseases = []
        for disease_id, disease_info in self.ontology["diseases"].items():
            if symptom in disease_info.get("symptoms", []):
                diseases.append({
                    "disease_id": disease_id,
                    "disease_name": disease_info["name"],
                    "severity": disease_info.get("severity")
                })
        return diseases
    
    def get_all_diseases(self):
        """Get list of all diseases"""
        return list(self.ontology["diseases"].keys())
    
    def get_all_symptoms(self):
        """Get list of all symptoms"""
        return list(self.ontology["symptoms"].keys())