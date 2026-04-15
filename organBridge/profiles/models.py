from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class DonorProfile(models.Model):
    ORGANS_CHOICES = [
        ('kidney', 'Kidney'),
        ('liver', 'Liver'),
        ('heart', 'Heart'),
        ('lungs', 'Lungs'),
        ('pancreas', 'Pancreas'),
        ('intestine', 'Intestine'),
        ('cornea', 'Cornea'),
        ('skin', 'Skin'),
        ('bone', 'Bone'),
    ]

    HEALTH_STATUS_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    SMOKING_CHOICES = [
        ('never', 'Never Smoked'),
        ('former', 'Former Smoker'),
        ('current', 'Current Smoker'),
    ]

    ALCOHOL_CHOICES = [
        ('never', 'Never'),
        ('occasional', 'Occasional'),
        ('regular', 'Regular'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='donor_profile')
    organs_donating = models.JSONField(default=list)
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, default='good')
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='never')
    alcohol_use = models.CharField(max_length=20, choices=ALCOHOL_CHOICES, default='never')
    drug_use = models.BooleanField(default=False)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    avg_sleep = models.FloatField(null=True, blank=True)
    last_medical_checkup = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    preferred_hospital = models.CharField(max_length=255, blank=True)
    insurance_provider = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    willing_to_travel = models.BooleanField(default=True)
    max_travel_distance = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.height and self.weight and self.height > 0:
            self.bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donor: {self.user.username}"

    def get_organs_list(self):
        return [dict(self.ORGANS_CHOICES).get(o, o) for o in self.organs_donating]


class RecipientProfile(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low - Can wait months'),
        ('medium', 'Medium - Needs within weeks'),
        ('high', 'High - Needs within days'),
        ('critical', 'Critical - Immediate need'),
    ]

    SMOKING_CHOICES = [
        ('never', 'Never Smoked'),
        ('former', 'Former Smoker'),
        ('current', 'Current Smoker'),
    ]

    ALCOHOL_CHOICES = [
        ('never', 'Never'),
        ('occasional', 'Occasional'),
        ('regular', 'Regular'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recipient_profile')
    organs_needed = models.JSONField(default=list)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    medical_condition = models.TextField(blank=True)
    diagnosis_date = models.DateField(null=True, blank=True)
    current_treatment = models.TextField(blank=True)
    current_hospital = models.CharField(max_length=100, blank=True)
    preferred_hospitals = models.JSONField(default=list, blank=True)
    previous_transplants = models.IntegerField(default=0)
    insurance_coverage = models.BooleanField(default=False)
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='never')
    alcohol_use = models.CharField(max_length=20, choices=ALCOHOL_CHOICES, default='never')
    drug_use = models.BooleanField(default=False)
    avg_sleep = models.FloatField(null=True, blank=True)
    preferred_hospital = models.CharField(max_length=255, blank=True)
    insurance_provider = models.CharField(max_length=255, blank=True)
    max_travel_distance = models.IntegerField(default=100)
    willing_to_relocate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recipient: {self.user.username}"

    def get_organs_list(self):
        return [dict(DonorProfile.ORGANS_CHOICES).get(o, o) for o in self.organs_needed]

    def get_urgency_color(self):
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'critical': 'darkred'
        }
        return colors.get(self.urgency_level, 'black')