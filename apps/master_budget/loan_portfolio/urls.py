from django.urls import path
from .views import (
    categories_loan_portfolio,
    category_loan_portfolio,
    scenarios_loan_portfolio,
    scenario_loan_portfolio,
    scenario_loan_portfolio_comments,
    scenarios_financial_investments,
    scenario_financial_investments,
    scenario_financial_investments_comments
)
urlpatterns = [
    path('categories/', categories_loan_portfolio, name="categories_loan_portfolio"),
    path(
        'categories/edit/<int:id>/',
        category_loan_portfolio,
        name="category_loan_portfolio"
    ),
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
    path(
        'financial-investments/scenarios/',
        scenarios_financial_investments,
        name="scenarios_financial_investments"
    ),
    path(
        'financial-investments/scenario/detail/<int:id>/',
        scenario_financial_investments,
        name="scenario_financial_investments"
    ),
    path(
        'financial-investments/scenario/detail/comments/<int:id>/',
        scenario_financial_investments_comments,
        name="scenario_financial_investments_comments"
    ),
]
