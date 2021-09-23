from django.urls import path
from apps.indirect_budgets.views import (
    indirect_budget_register,
    generate_excel_file,
)

urlpatterns = [
    path(
        'indirect-budget-register/',
        indirect_budget_register,
        name='indirect_budget_register'
    ),
    path(
        'generate-excel-file/<int:period>/<int:account>/',
        generate_excel_file,
        name='generate_excel_file'
    ),
]
