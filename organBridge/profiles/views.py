from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonorProfile, RecipientProfile
from .forms import DonorProfileForm, RecipientProfileForm


def home(request):
    return render(request, 'profiles/home.html')


@login_required
def profile_dashboard(request):
    user = request.user
    try:
        if user.user_type == 'donor':
            if DonorProfile.objects.filter(user=user).exists():
                return donor_dashboard(request)
            else:
                messages.info(request, 'Please complete your donor profile first.')
                return redirect('profiles:profile_setup')
        elif user.user_type == 'recipient':
            if RecipientProfile.objects.filter(user=user).exists():
                return recipient_dashboard(request)
            else:
                messages.info(request, 'Please complete your recipient profile first.')
                return redirect('profiles:profile_setup')
    except Exception as e:
        messages.error(request, 'Something went wrong.')
        return redirect('profiles:profile_setup')


@login_required
def donor_dashboard(request):
    donor = DonorProfile.objects.get(user=request.user)
    context = {
        'donor': donor,
        'organs_count': len(donor.organs_donating),
    }
    return render(request, 'profiles/donor_dashboard.html', context)


@login_required
def recipient_dashboard(request):
    recipient = RecipientProfile.objects.get(user=request.user)
    context = {
        'recipient': recipient,
        'organs_count': len(recipient.organs_needed),
        'urgency_color': recipient.get_urgency_color(),
    }
    return render(request, 'profiles/recipient_dashboard.html', context)


@login_required
def profile_setup(request):
    user = request.user

    # Check if profile already exists — direct dashboard pe bhejo
    if user.user_type == 'donor':
        if DonorProfile.objects.filter(user=user).exists():
            return redirect('profiles:donor_dashboard')
        form_class = DonorProfileForm
    elif user.user_type == 'recipient':
        if RecipientProfile.objects.filter(user=user).exists():
            return redirect('profiles:recipient_dashboard')
        form_class = RecipientProfileForm
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile setup complete!')
            if user.user_type == 'donor':
                return redirect('profiles:donor_dashboard')
            return redirect('profiles:recipient_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = form_class()

    return render(request, 'profiles/profile_setup.html', {
        'form': form,
        'user_type': user.user_type,
    })

@login_required
def edit_profile(request):
    user = request.user

    if user.user_type == 'donor':
        profile = DonorProfile.objects.get(user=user)
        form_class = DonorProfileForm
        template = 'profiles/edit_donor_profile.html'
    else:
        profile = RecipientProfile.objects.get(user=user)
        form_class = RecipientProfileForm
        template = 'profiles/edit_recipient_profile.html'

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profiles:profile_dashboard')
    else:
        form = form_class(instance=profile)

    return render(request, template, {'form': form})