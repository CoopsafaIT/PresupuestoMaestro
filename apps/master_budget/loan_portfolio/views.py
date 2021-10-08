from django.shortcuts import render


def scenarios(request):
    ctx = {}
    return render(request, 'loan_portfolio/scenarios.html', ctx)
