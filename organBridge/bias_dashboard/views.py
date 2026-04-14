from django.shortcuts import render


def bias_overview(request):
    return render(request, 'bias_dashboard/overview.html')