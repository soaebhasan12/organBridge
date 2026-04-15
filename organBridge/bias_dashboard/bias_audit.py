import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


class BiasAuditor:

    def __init__(self):
        self.results = {}

    def audit_matches(self, matches_data):
        """
        matches_data = list of dicts:
        {
            'donor_gender': 'male',
            'donor_age': 25,
            'donor_city': 'Delhi',
            'recipient_gender': 'female',
            'recipient_age': 30,
            'recipient_city': 'Mumbai',
            'match_score': 85.5,
            'blood_compatible': True,
        }
        """
        if not matches_data:
            return self._empty_results()

        df = pd.DataFrame(matches_data)

        results = {
            'total_matches': len(df),
            'gender_bias': self._check_gender_bias(df),
            'age_bias': self._check_age_bias(df),
            'location_bias': self._check_location_bias(df),
            'overall_fairness_score': 0,
        }

        # Overall fairness score (0-100, higher = fairer)
        scores = [
            results['gender_bias']['fairness_score'],
            results['age_bias']['fairness_score'],
            results['location_bias']['fairness_score'],
        ]
        results['overall_fairness_score'] = round(np.mean(scores), 2)

        self.results = results
        return results

    def _check_gender_bias(self, df):
        try:
            if 'donor_gender' not in df.columns:
                return {'fairness_score': 100, 'details': 'No gender data'}

            gender_scores = df.groupby('donor_gender')['match_score'].mean()
            max_diff = float(gender_scores.max() - gender_scores.min())
            fairness_score = max(0, 100 - (max_diff * 2))

            return {
                'fairness_score': round(fairness_score, 2),
                'avg_scores_by_gender': gender_scores.to_dict(),
                'max_difference': round(max_diff, 2),
                'status': 'fair' if fairness_score >= 80 else 'biased',
            }
        except Exception:
            return {'fairness_score': 100, 'details': 'Could not analyze'}

    def _check_age_bias(self, df):
        try:
            if 'donor_age' not in df.columns:
                return {'fairness_score': 100, 'details': 'No age data'}

            df['age_group'] = pd.cut(
                df['donor_age'],
                bins=[0, 30, 45, 60, 100],
                labels=['18-30', '31-45', '46-60', '60+']
            )
            age_scores = df.groupby('age_group', observed=True)['match_score'].mean()
            max_diff = float(age_scores.max() - age_scores.min())
            fairness_score = max(0, 100 - (max_diff * 1.5))

            return {
                'fairness_score': round(fairness_score, 2),
                'avg_scores_by_age_group': age_scores.to_dict(),
                'max_difference': round(max_diff, 2),
                'status': 'fair' if fairness_score >= 80 else 'biased',
            }
        except Exception:
            return {'fairness_score': 100, 'details': 'Could not analyze'}

    def _check_location_bias(self, df):
        try:
            if 'donor_city' not in df.columns:
                return {'fairness_score': 100, 'details': 'No location data'}

            city_scores = df.groupby('donor_city')['match_score'].mean()
            max_diff = float(city_scores.max() - city_scores.min())
            fairness_score = max(0, 100 - (max_diff * 1.5))

            return {
                'fairness_score': round(fairness_score, 2),
                'top_cities': city_scores.nlargest(5).to_dict(),
                'max_difference': round(max_diff, 2),
                'status': 'fair' if fairness_score >= 80 else 'biased',
            }
        except Exception:
            return {'fairness_score': 100, 'details': 'Could not analyze'}

    def _empty_results(self):
        return {
            'total_matches': 0,
            'gender_bias': {'fairness_score': 100, 'status': 'no data'},
            'age_bias': {'fairness_score': 100, 'status': 'no data'},
            'location_bias': {'fairness_score': 100, 'status': 'no data'},
            'overall_fairness_score': 100,
        }

    def get_summary(self):
        if not self.results:
            return "No audit performed yet."

        score = self.results.get('overall_fairness_score', 0)
        if score >= 90:
            label = "Excellent"
        elif score >= 80:
            label = "Good"
        elif score >= 70:
            label = "Fair"
        else:
            label = "Needs Improvement"

        return {
            'overall_score': score,
            'label': label,
            'total_matches_analyzed': self.results.get('total_matches', 0),
        }