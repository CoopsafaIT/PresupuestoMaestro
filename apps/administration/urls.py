
from django.urls import path
from apps.administration.views import (
    inflationary_index,
    cost_centers,
    investment_accounts,
    investment_account,
    investments,
    investment,
    job_positions,
    job_position,
    projects,
    projections,
    periods,
    period,
    budget_init,
    control_budgeted_cost_centers
)

urlpatterns = [
    path('inflationary-index/', inflationary_index, name="inflationary_index"),
    path('cost-centers/', cost_centers, name="cost_centers"),
    path('budget-init/', budget_init, name="budget_init"),
    path('investment-accounts/', investment_accounts, name="investment_accounts"),
    path('investment-account/<int:id>/', investment_account, name="investment_account"),
    path('investments/', investments, name="investments"),
    path('investment/<int:id>/', investment, name="investment"),
    path('job-positions/', job_positions, name="job_positions"),
    path('job-position/<int:id>/', job_position, name="job_position"),
    path('projects/', projects, name="projects"),
    path('projections/', projections, name="projections"),
    path('periods/', periods, name="periods"),
    path('period/<int:id>/', period, name="period"),
    path('control-budgeted-cost-centers/', control_budgeted_cost_centers, name="control_budgeted_cost_centers"),
]
