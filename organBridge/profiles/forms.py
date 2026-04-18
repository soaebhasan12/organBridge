from django import forms
from .models import DonorProfile, RecipientProfile


class DonorProfileForm(forms.ModelForm):
    organs_donating = forms.MultipleChoiceField(
        choices=DonorProfile.ORGANS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = DonorProfile
        exclude = ['user', 'bmi', 'created_at', 'updated_at']
        widgets = {
            'last_medical_checkup': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_organs_donating(self):
        return list(self.cleaned_data['organs_donating'])


class RecipientProfileForm(forms.ModelForm):
    organs_needed = forms.MultipleChoiceField(
        choices=DonorProfile.ORGANS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = RecipientProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_condition': forms.Textarea(attrs={'rows': 3}),
            'current_treatment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_organs_needed(self):
        return list(self.cleaned_data['organs_needed'])