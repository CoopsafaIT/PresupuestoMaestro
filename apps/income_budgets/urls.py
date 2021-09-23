from django.urls import path
from apps.income_budgets.views import (
    income_budget_register,
    income_budget_generate_excel_file,
)

urlpatterns = [
    path(
        'income-budget-register/',
        income_budget_register,
        name='income_budget_register'
    ),
    path(
        'generate-excel-file/<int:period>/<int:account>/',
        income_budget_generate_excel_file,
        name='income_budget_generate_excel_file'
    ),
]
