from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import DonorProfile, RecipientProfile
from ml_model.matching_algorithm import OrganMatchingEngine
from .models import OrganMatch, MatchPreference


@login_required
def find_matches(request):
    """
    Recipient ke liye ML-based donor matches dhundhta hai.
    Sirf recipients access kar sakte hain.
    """
    if not request.user.is_recipient():
        messages.error(request, 'Only recipients can search for matches.')
        return redirect('profiles:profile_dashboard')

    try:
        recipient = RecipientProfile.objects.get(user=request.user)
    except RecipientProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('profiles:profile_setup')

    # Available donors fetch karo
    donors = DonorProfile.objects.filter(is_available=True).select_related('user')

    if not donors.exists():
        return render(request, 'matches/find_matches.html', {
            'matches': [],
            'recipient': recipient,
            'message': 'No donors available at the moment.'
        })

    # ML engine se matches nikalo
    engine = OrganMatchingEngine()
    matches_data = engine.find_matches(recipient, donors, top_n=10)

    # OrganMatch records create/update karo
    formatted_matches = []
    for match in matches_data:
        donor_user = match['donor'].user
        organ_match, created = OrganMatch.objects.get_or_create(
            donor=donor_user,
            recipient=request.user,
            defaults={
                'match_score': match['final_score'],
                'organs_matched': match['organs_matched'],
            }
        )
        if not created:
            organ_match.match_score = match['final_score']
            organ_match.organs_matched = match['organs_matched']
            organ_match.save()

        formatted_matches.append({
            'donor': match['donor'],
            'donor_user': donor_user,
            'ml_score': match['ml_score'],
            'final_score': match['final_score'],
            'organs_matched': match['organs_matched'],
            'blood_compatible': match['blood_compatible'],
            'match_obj': organ_match,
        })

    return render(request, 'matches/find_matches.html', {
        'matches': formatted_matches,
        'recipient': recipient,
        'total': len(formatted_matches),
    })


@login_required
def my_matches(request):
    """
    User ke saare matches dikhata hai — donor aur recipient dono ke liye.
    """
    user = request.user
    if user.is_donor():
        matches = OrganMatch.objects.filter(donor=user).select_related('recipient')
    else:
        matches = OrganMatch.objects.filter(recipient=user).select_related('donor')

    return render(request, 'matches/my_matches.html', {
        'matches': matches,
        'user_type': user.user_type,
    })


@login_required
def update_match_status(request, match_id, status):
    """
    Match ko accept ya reject karne ke liye.
    """
    match = get_object_or_404(OrganMatch, id=match_id)

    if request.user not in [match.donor, match.recipient]:
        messages.error(request, 'Permission denied.')
        return redirect('matches:my_matches')

    if status in ['accepted', 'rejected']:
        match.status = status
        match.save()
        messages.success(request, f'Match {status}!')

    return redirect('matches:my_matches')