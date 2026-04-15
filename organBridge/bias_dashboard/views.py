from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from matches.models import OrganMatch
from .bias_audit import BiasAuditor


@login_required
def bias_overview(request):
    # Get all matches data
    matches = OrganMatch.objects.select_related(
        'donor', 'recipient'
    ).all()

    matches_data = []
    for match in matches:
        matches_data.append({
            'donor_gender': match.donor.gender,
            'donor_age': match.donor.age or 0,
            'donor_city': match.donor.city,
            'recipient_gender': match.recipient.gender,
            'recipient_age': match.recipient.age or 0,
            'recipient_city': match.recipient.city,
            'match_score': match.match_score,
            'blood_compatible': True,
        })

    auditor = BiasAuditor()
    audit_results = auditor.audit_matches(matches_data)
    summary = auditor.get_summary()

    return render(request, 'bias_dashboard/overview.html', {
        'audit_results': audit_results,
        'summary': summary,
        'total_matches': len(matches_data),
    })