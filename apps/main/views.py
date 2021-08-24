from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def error_404(request, exception=None):
    return render(request, 'errors/404.html', {})


def error_500(request, exception=None):
    return render(request, 'errors/404.html', {})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})
