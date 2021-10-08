from django.urls import path
from apps.main.views import (
    dashboard,
    budget_execution_report
)

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path(
        'budget-execution-report/',
        budget_execution_report,
        name="budget_execution_report"
    ),
]
