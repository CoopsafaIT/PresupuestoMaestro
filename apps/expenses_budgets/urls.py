from django.urls import path
from apps.expenses_budgets.views import (
    budget_register,
    user_create_project,
    get_projects_by_cost_center,
    generate_excel_report,
    transfers_expenses
)

urlpatterns = [
    path('budget-register/', budget_register, name='budget_register'),
    path('user-create-project/', user_create_project, name='user_create_project'),
    path(
        'generate-excel-report/<int:project>/<int:period>/<int:cost_center>/',
        generate_excel_report,
        name='generate_excel_report'
    ),
    path(
        'ajax-get-projects-by-cost-center/',
        get_projects_by_cost_center,
        name='get_projects_by_cost_center'
    ),
    path(
        'transfers/',
        transfers_expenses,
        name='transfers_expenses'
    ),
]
