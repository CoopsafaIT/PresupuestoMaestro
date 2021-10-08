from django.urls import path
from apps.master_budget.views import master_budget_dashboard

urlpatterns = [
    path('', master_budget_dashboard, name="master_budget_dashboard"),
]
