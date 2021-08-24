from django.urls import path
from apps.staff_budgets.views import (
    staff_budgets_register,
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
]
