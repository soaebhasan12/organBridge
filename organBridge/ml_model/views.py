from django.shortcuts import render


def model_status(request):
    return render(request, 'ml_model/status.html')