from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'profiles/home.html')


@login_required
def profile_dashboard(request):
    return render(request, 'profiles/dashboard.html')


@login_required
def profile_setup(request):
    return render(request, 'profiles/profile_setup.html')


@login_required
def edit_profile(request):
    return render(request, 'profiles/edit_profile.html')