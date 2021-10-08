from django.shortcuts import render


def master_budget_dashboard(request):
    ctx = {}
    return render(request, 'master_budget/dashboard.html', ctx)
