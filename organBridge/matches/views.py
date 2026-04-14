from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def find_matches(request):
    return render(request, 'matches/find_matches.html')


@login_required
def my_matches(request):
    return render(request, 'matches/my_matches.html')