import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'trained_models')


class OrganMatchingEngine:

    def __init__(self):
        self.tf_model = None
        self.tf_matrix = None
        self.cosine_sim = None
        self._load_models()

    def _load_models(self):
        try:
            tf_model_path = os.path.join(MODEL_PATH, 'tf_model.pkl')
            tf_matrix_path = os.path.join(MODEL_PATH, 'tf_matrix.npy')
            cosine_sim_path = os.path.join(MODEL_PATH, 'cosine_sim.npy')

            if not all(os.path.exists(p) for p in [tf_model_path, tf_matrix_path, cosine_sim_path]):
                print("Model files not found — using rule-based fallback.")
                return

            with open(tf_model_path, 'rb') as f:
                self.tf_model = pickle.load(f)

            self.tf_matrix = np.load(tf_matrix_path)
            self.cosine_sim = np.load(cosine_sim_path)
            print("ML models loaded successfully!")

        except Exception as e:
            print(f"Error loading models: {e}")
            self.tf_model = None

    def prepare_donor_string(self, donor):
        user = donor.user
        return (
            f"{user.city} {user.gender} {user.race} {user.age} "
            f"{user.blood_type} {donor.health_status} "
            f"{donor.smoking_status} {donor.alcohol_use} "
            f"{'drug' if donor.drug_use else 'nodrug'} "
            f"{' '.join(donor.organs_donating)}"
        )

    def prepare_recipient_string(self, recipient):
        user = recipient.user
        return (
            f"{user.city} {user.gender} {user.race} {user.age} "
            f"{user.blood_type} {recipient.urgency_level} "
            f"{recipient.smoking_status} {recipient.alcohol_use} "
            f"{'drug' if recipient.drug_use else 'nodrug'} "
            f"{' '.join(recipient.organs_needed)}"
        )

    def calculate_ml_score(self, donor, recipient):
        try:
            if self.tf_model is None:
                return self.calculate_rule_score(donor, recipient)

            donor_str = self.prepare_donor_string(donor)
            recipient_str = self.prepare_recipient_string(recipient)

            donor_vec = self.tf_model.transform([donor_str]).toarray()
            recipient_vec = self.tf_model.transform([recipient_str]).toarray()

            similarity = cosine_similarity(donor_vec, recipient_vec)[0][0]
            return round(max(0, min(100, similarity * 100)), 2)

        except Exception as e:
            print(f"ML score failed: {e}")
            return self.calculate_rule_score(donor, recipient)

    def calculate_rule_score(self, donor, recipient):
        score = 0

        # Blood type compatibility (40 points)
        if self.is_blood_compatible(donor.user.blood_type, recipient.user.blood_type):
            score += 40

        # Organ match (30 points)
        donor_organs = self._get_organ_list(donor.organs_donating)
        recipient_organs = self._get_organ_list(recipient.organs_needed)
        matched = set(donor_organs) & set(recipient_organs)
        if matched:
            score += 30

        # Location match (15 points)
        if donor.user.city and recipient.user.city:
            if donor.user.city.lower() == recipient.user.city.lower():
                score += 15
            elif donor.user.state and recipient.user.state:
                if donor.user.state.lower() == recipient.user.state.lower():
                    score += 8

        # Health status (15 points)
        health_scores = {'excellent': 15, 'good': 10, 'fair': 5, 'poor': 0}
        score += health_scores.get(donor.health_status, 0)

        return min(100, score)

    def is_blood_compatible(self, donor_blood, recipient_blood):
        compatibility = {
            'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
            'O+': ['O+', 'A+', 'B+', 'AB+'],
            'A-': ['A-', 'A+', 'AB-', 'AB+'],
            'A+': ['A+', 'AB+'],
            'B-': ['B-', 'B+', 'AB-', 'AB+'],
            'B+': ['B+', 'AB+'],
            'AB-': ['AB-', 'AB+'],
            'AB+': ['AB+'],
        }
        return recipient_blood in compatibility.get(donor_blood, [])

    def _get_organ_list(self, organs_field):
        if isinstance(organs_field, list):
            return [str(o) for o in organs_field]
        elif isinstance(organs_field, str):
            return [o.strip() for o in organs_field.split(',') if o.strip()]
        return []

    def get_urgency_multiplier(self, urgency_level):
        multipliers = {
            'critical': 1.3,
            'high': 1.2,
            'medium': 1.1,
            'low': 1.0,
        }
        return multipliers.get(urgency_level, 1.0)

    def find_matches(self, recipient, donors, top_n=10):
        matches = []
        recipient_organs = self._get_organ_list(recipient.organs_needed)

        for donor in donors:
            donor_organs = self._get_organ_list(donor.organs_donating)
            organs_matched = [o for o in donor_organs if o in recipient_organs]

            if not organs_matched:
                continue

            ml_score = self.calculate_ml_score(donor, recipient)
            urgency_multiplier = self.get_urgency_multiplier(recipient.urgency_level)
            final_score = min(100, round(ml_score * urgency_multiplier, 2))

            matches.append({
                'donor': donor,
                'ml_score': ml_score,
                'final_score': final_score,
                'organs_matched': organs_matched,
                'blood_compatible': self.is_blood_compatible(
                    donor.user.blood_type,
                    recipient.user.blood_type
                ),
            })

        matches.sort(key=lambda x: x['final_score'], reverse=True)
        return matches[:top_n]