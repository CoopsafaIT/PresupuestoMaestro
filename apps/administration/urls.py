
from django.urls import path
from apps.administration.views import (
    inflationary_index,
    cost_centers,
    investment_accounts,
    investment_account,
    investments,
    investment,
    job_positions,
    job_position
)

urlpatterns = [
    path('inflationary-index/', inflationary_index, name="inflationary_index"),
    path('cost-centers/', cost_centers, name="cost_centers"),
    path('investment-accounts/', investment_accounts, name="investment_accounts"),
    path('investment-account/<int:id>/', investment_account, name="investment_account"),
    path('investments/', investments, name="investments"),
    path('investment/<int:id>/', investment, name="investment"),
    path('job_positions/', job_positions, name="job_positions"),
    path('job_position/<int:id>/', job_position, name="job_position"),
]
