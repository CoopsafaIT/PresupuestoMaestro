from django.urls import path
from apps.investment_budgets.views import (
    investment_budget_register,
    investement_budget_delete,
    investment_budget_update,
    get_investment_by_account,
    generate_excel_report,
    check_out_investment,
    transfers_investment,
)

urlpatterns = [
    path(
        'investment-budget-register/',
        investment_budget_register,
        name='investment_budget_register'
    ),
    path(
        'investement-budget-update/<int:id>/',
        investment_budget_update,
        name='investment_budget_update'
    ),
    path(
        'investement-budget-delete/<int:id>/',
        investement_budget_delete,
        name='investement_budget_delete'
    ),
    path(
        'get-investment-by-account/<int:account_id>',
        get_investment_by_account,
        name='get_investment_by_account'
    ),
    path(
        'generate-excel-report/<int:period>/<int:cost_center>/',
        generate_excel_report,
        name='generate_excel_report'
    ),
    path(
        'check-out/',
        check_out_investment,
        name='check_out_investment'
    ),
    path(
        'transfers/',
        transfers_investment,
        name='transfers_investment'
    ),
]
