from django.urls import path
from apps.cost_budgets.views import (
    cost_budget_register,
    cost_budget_generate_excel_file,
)

urlpatterns = [
    path(
        'cost-budget-register/',
        cost_budget_register,
        name='cost_budget_register'
    ),
    path(
        'generate-excel-file/<int:period>/<int:account>/',
        cost_budget_generate_excel_file,
        name='cost_budget_generate_excel_file'
    ),
]
