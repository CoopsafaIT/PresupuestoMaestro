from django.urls import path
from apps.staff_budgets.views import (
    staff_budgets_register,
    staff_budgets_update,
    staff_budgets_delete,
    generate_excel_report
)

urlpatterns = [
    path(
        'staff-budgets-register/',
        staff_budgets_register,
        name='staff_budgets_register'
    ),
    path(
        'generate-excel-report/<int:period>/<int:cost_center>/',
        generate_excel_report,
        name='generate_excel_report'
    ),
    path(
        'staff-budget-delete/<int:id>/',
        staff_budgets_delete,
        name='staff_budgets_delete'
    ),
    path(
        'staff-budget-update/<int:id>/',
        staff_budgets_update,
        name='staff_budgets_update'
    ),
]
