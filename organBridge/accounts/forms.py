from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES)
    blood_type = forms.ChoiceField(choices=CustomUser.BLOOD_TYPE_CHOICES)
    race = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'phone_number', 'date_of_birth',
                  'age', 'gender', 'blood_type', 'race', 'city', 'state', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))