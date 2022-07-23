from django.urls import path
from . import views

urlpatterns = [
    path(
        'savings-liabilities/scenarios/',
        views.scenarios_savings_liabilities,
        name="scenarios_savings_liabilities"
    ),
    path(
        'savings-liabilities/scenario/detail/<int:id>/',
        views.scenario_savings_liabilities,
        name="scenario_savings_liabilities"
    ),
    path(
        'savings-liabilities/scenario/detail/comments/<int:id>/',
        views.scenario_savings_liabilities_comments,
        name="scenario_savings_liabilities_comments"
    ),
    path(
        'liabilities-loans/scenarios/',
        views.scenarios_liabilities_loans,
        name="scenarios_liabilities_loans"
    ),
    path(
        'liabilities-loans/scenario/detail/<int:id>/',
        views.scenario_liabilities_loans,
        name="scenario_liabilities_loans"
    ),
    path(
        'liabilities-loans/scenario/detail/comments/<int:id>/',
        views.scenario_liabilities_loans_comments,
        name="scenario_liabilities_loans_comments"
    ),
    path(
        'others-passives/scenarios/', views.scenarios_others_passives, name="scenarios_others_passives" # NOQA
    ),
    path(
        'others-passives/scenario/detail/<int:id>/',
        views.scenario_others_passives,
        name="scenario_others_passives"
    ),
]
