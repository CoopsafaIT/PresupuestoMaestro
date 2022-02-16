from django.urls import path
from apps.travel_budgets.views import (
    travel_budget_register,
    travel_budget_update,
    travel_budget_delete,
    generate_excel_report,
    check_out_travel,
    load_travel_distribution
)

urlpatterns = [
    path(
        'travel-budget-register/',
        travel_budget_register,
        name='travel_budget_register'
    ),
    path(
        'travel-budget-update/<int:id>/',
        travel_budget_update,
        name='travel_budget_update'
    ),
    path(
        'travel-budget-delete/<int:id>/',
        travel_budget_delete,
        name='travel_budget_delete'
    ),
    path(
        'generate-excel-report/<int:period>/<int:cost_center>/',
        generate_excel_report,
        name='generate_excel_report'
    ),
    path(
        'check-out/',
        check_out_travel,
        name='check_out_travel'
    ),
    path(
        'load-travel-distribution/',
        load_travel_distribution,
        name='load_travel_distribution'
    ),
]
