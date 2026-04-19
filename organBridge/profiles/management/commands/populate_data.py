import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import DonorProfile, RecipientProfile
from matches.models import OrganMatch

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample donor/recipient data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad',
                  'Pune', 'Kolkata', 'Roorkee', 'Dehradun', 'Jaipur']
        states = ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu',
                  'Telangana', 'Maharashtra', 'West Bengal', 'Uttarakhand',
                  'Uttarakhand', 'Rajasthan']
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        genders = ['male', 'female']
        organs = ['kidney', 'liver', 'heart', 'lungs', 'cornea', 'pancreas']
        health_statuses = ['excellent', 'good', 'fair']
        smoking_choices = ['never', 'former', 'current']
        alcohol_choices = ['never', 'occasional', 'regular']
        urgency_choices = ['low', 'medium', 'high', 'critical']

        # Create 20 donors
        donors_created = 0
        for i in range(1, 41):
            username = f'donor_{i}'
            if CustomUser.objects.filter(username=username).exists():
                continue

            city_idx = random.randint(0, len(cities)-1)
            user = CustomUser.objects.create_user(
                username=username,
                password='Test@1234',
                email=f'donor{i}@test.com',
                user_type='donor',
                blood_type=random.choice(blood_types),
                gender=random.choice(genders),
                age=random.randint(18, 55),
                city=cities[city_idx],
                state=states[city_idx],
            )

            organ_list = random.sample(organs, random.randint(1, 3))
            DonorProfile.objects.create(
                user=user,
                organs_donating=organ_list,
                health_status=random.choice(health_statuses),
                smoking_status=random.choice(smoking_choices),
                alcohol_use=random.choice(alcohol_choices),
                drug_use=random.choice([True, False]),
                height=random.uniform(155, 185),
                weight=random.uniform(50, 90),
                avg_sleep=random.uniform(5, 9),
                is_available=True,
                willing_to_travel=random.choice([True, False]),
                max_travel_distance=random.choice([50, 100, 200, 500]),
            )
            donors_created += 1

        # Create 20 recipients
        recipients_created = 0
        for i in range(1, 41):
            username = f'recipient_{i}'
            if CustomUser.objects.filter(username=username).exists():
                continue

            city_idx = random.randint(0, len(cities)-1)
            user = CustomUser.objects.create_user(
                username=username,
                password='Test@1234',
                email=f'recipient{i}@test.com',
                user_type='recipient',
                blood_type=random.choice(blood_types),
                gender=random.choice(genders),
                age=random.randint(18, 65),
                city=cities[city_idx],
                state=states[city_idx],
            )

            organ_list = random.sample(organs, random.randint(1, 2))
            RecipientProfile.objects.create(
                user=user,
                organs_needed=organ_list,
                urgency_level=random.choice(urgency_choices),
                medical_condition='Sample medical condition',
                current_hospital=f'Hospital {i}',
                smoking_status=random.choice(smoking_choices),
                alcohol_use=random.choice(alcohol_choices),
                drug_use=random.choice([True, False]),
                avg_sleep=random.uniform(5, 9),
                max_travel_distance=random.choice([50, 100, 200]),
            )
            recipients_created += 1

        # Create sample matches
        matches_created = 0
        donors = list(DonorProfile.objects.all()[:10])
        recipients = list(RecipientProfile.objects.all()[:10])

        for recipient in recipients:
            for donor in random.sample(donors, min(3, len(donors))):
                if OrganMatch.objects.filter(
                    donor=donor.user,
                    recipient=recipient.user
                ).exists():
                    continue

                organs_matched = list(
                    set(donor.organs_donating) &
                    set(recipient.organs_needed)
                )
                if not organs_matched:
                    organs_matched = ['kidney']

                OrganMatch.objects.create(
                    donor=donor.user,
                    recipient=recipient.user,
                    match_score=round(random.uniform(30, 95), 2),
                    organs_matched=organs_matched,
                    status=random.choice(['pending', 'accepted', 'rejected']),
                )
                matches_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Donors: {donors_created}, Recipients: {recipients_created}, Matches: {matches_created}'
        ))