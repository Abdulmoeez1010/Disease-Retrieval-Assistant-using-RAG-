"""
Medical Reasoning Engine
Performs inference and reasoning over medical knowledge
"""

import re
from collections import defaultdict


class MedicalReasoningEngine:
    def __init__(self, ontology):
        self.ontology = ontology
    
    def extract_symptoms_from_text(self, text):
        """
        Extract symptoms from user's text using simple NLP
        """
        text_lower = text.lower()
        extracted_symptoms = []
        
        # Get all symptoms from ontology
        all_symptoms = self.ontology.ontology["symptoms"]
        
        # Symptom mapping (casual language → ontology terms)
        symptom_mappings = {
            "fever": "high_fever",
            "temperature": "high_fever",
            "headache": "severe_headache",
            "head pain": "severe_headache",
            "rash": "skin_rash",
            "red spots": "skin_rash",
            "spots on skin": "skin_rash",
            "joint pain": "joint_pain",
            "body ache": "joint_pain",
            "muscle pain": "muscle_pain",
            "eye pain": "pain_behind_eyes",
            "pain behind eyes": "pain_behind_eyes",
            "nausea": "nausea",
            "vomiting": "vomiting",
            "throw up": "vomiting",
            "runny nose": "runny_nose",
            "sneezing": "sneezing",
            "cough": "cough",
            "sore throat": "sore_throat",
            "chills": "chills",
            "sweating": "sweating",
            "fatigue": "fatigue",
            "tired": "fatigue"
        }
        
        # Extract symptoms
        for casual_term, ontology_term in symptom_mappings.items():
            if casual_term in text_lower:
                if ontology_term not in extracted_symptoms:
                    extracted_symptoms.append(ontology_term)
        
        return extracted_symptoms
    
    def reason_about_diseases(self, symptoms):
        """
        Main reasoning function: Given symptoms, infer possible diseases
        """
        if not symptoms:
            return []
        
        disease_scores = defaultdict(lambda: {"score": 0, "matched_symptoms": [], "confidence": 0})
        
        # Score each disease based on symptom matches
        for disease_id, disease_info in self.ontology.ontology["diseases"].items():
            disease_symptoms = disease_info.get("symptoms", [])
            
            # Calculate match score
            matched = set(symptoms) & set(disease_symptoms)
            if matched:
                score = len(matched) / len(disease_symptoms)
                disease_scores[disease_id] = {
                    "score": score,
                    "matched_symptoms": list(matched),
                    "confidence": score,
                    "disease_name": disease_info["name"],
                    "severity": disease_info.get("severity"),
                    "all_symptoms": disease_symptoms,
                    "requires_immediate_care": disease_info.get("requires_immediate_care", False)
                }
        
        # Apply reasoning rules
        rule_inferences = self._apply_rules(symptoms)
        
        # Merge rule-based inferences with symptom matching
        for inference in rule_inferences:
            disease_id = inference["conclusion"]
            if disease_id in disease_scores:
                # Boost confidence if rule also matches
                disease_scores[disease_id]["confidence"] = max(
                    disease_scores[disease_id]["confidence"],
                    inference["confidence"]
                )
            else:
                # Add from rule even if not matched by symptoms
                disease_info = self.ontology.get_disease_info(disease_id)
                if disease_info:
                    disease_scores[disease_id] = {
                        "score": inference["confidence"],
                        "matched_symptoms": symptoms,
                        "confidence": inference["confidence"],
                        "disease_name": disease_info["name"],
                        "severity": disease_info.get("severity"),
                        "all_symptoms": disease_info.get("symptoms", []),
                        "requires_immediate_care": disease_info.get("requires_immediate_care", False),
                        "inferred_by_rule": inference["rule_name"]
                    }
        
        # Sort by confidence
        sorted_diseases = sorted(
            disease_scores.items(),
            key=lambda x: x[1]["confidence"],
            reverse=True
        )
        
        return [
            {
                "disease_id": disease_id,
                **disease_data
            }
            for disease_id, disease_data in sorted_diseases
        ]
    
    def _apply_rules(self, symptoms):
        """
        Apply reasoning rules from ontology
        """
        inferences = []
        rules = self.ontology.ontology.get("rules", [])
        
        for rule in rules:
            condition = rule["condition"]
            
            # Check "all_of" conditions
            all_of = condition.get("all_of", [])
            all_match = all(symptom in symptoms for symptom in all_of)
            
            # Check "any_of" conditions
            any_of = condition.get("any_of", [])
            any_match = any(symptom in symptoms for symptom in any_of) if any_of else True
            
            # If rule conditions are met
            if all_match and any_match:
                inferences.append({
                    "conclusion": rule["conclusion"],
                    "confidence": rule["confidence"],
                    "rule_name": rule["name"]
                })
        
        return inferences
    
    def check_urgency(self, symptoms, disease_candidates):
        """
        Determine if immediate medical attention is needed
        """
        urgency_reasons = []
        
        # Check disease severity
        for disease in disease_candidates[:3]:  # Top 3 candidates
            if disease.get("requires_immediate_care"):
                urgency_reasons.append(
                    f"{disease['disease_name']} requires immediate medical attention"
                )
        
        # Check symptom severity
        for symptom in symptoms:
            symptom_info = self.ontology.get_symptom_info(symptom)
            if symptom_info and symptom_info.get("severity_indicator"):
                urgency_reasons.append(
                    f"{symptom_info['name']} is a severe symptom"
                )
        
        is_urgent = len(urgency_reasons) > 0
        
        return {
            "is_urgent": is_urgent,
            "reasons": urgency_reasons
        }
    
    def get_treatment_recommendations(self, disease_id):
        """
        Get treatment recommendations for a disease
        """
        disease_info = self.ontology.get_disease_info(disease_id)
        if not disease_info:
            return []
        
        return disease_info.get("treatments", [])
    
    def explain_reasoning(self, symptoms, disease_candidates):
        """
        Generate human-readable explanation of reasoning
        """
        if not disease_candidates:
            return "Based on the symptoms, I couldn't identify a specific condition."
        
        top_disease = disease_candidates[0]
        explanation = []
        
        explanation.append(
            f"Based on your symptoms ({', '.join(symptoms)}), "
            f"the most likely condition is **{top_disease['disease_name']}** "
            f"(confidence: {top_disease['confidence']*100:.0f}%)."
        )
        
        explanation.append(
            f"\nYour symptoms match {len(top_disease['matched_symptoms'])} out of "
            f"{len(top_disease['all_symptoms'])} typical symptoms of {top_disease['disease_name']}."
        )
        
        if len(disease_candidates) > 1:
            other_possibilities = [d['disease_name'] for d in disease_candidates[1:3]]
            explanation.append(
                f"\nOther possible conditions include: {', '.join(other_possibilities)}."
            )
        
        return "\n".join(explanation)