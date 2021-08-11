from django.shortcuts import render


def error_404(request, exception=None):
    return render(request, 'errors/404.html', {})


def error_500(request, exception=None):
    return render(request, 'errors/404.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {})
