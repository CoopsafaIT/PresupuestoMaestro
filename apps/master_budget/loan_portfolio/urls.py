from django.urls import path
from .views import (
    scenarios_loan_portfolio,
    scenario_loan_portfolio,
    scenario_loan_portfolio_comments
)
urlpatterns = [
    path('scenarios/', scenarios_loan_portfolio, name="scenarios_loan_portfolio"),
    path(
        'scenario/detail/<int:id>/',
        scenario_loan_portfolio,
        name="scenario_loan_portfolio"
    ),
    path(
        'scenario/detail/comments/<int:id>/',
        scenario_loan_portfolio_comments,
        name="scenario_loan_portfolio_comments"
    ),
]
