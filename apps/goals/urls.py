from django.urls import path
from apps.goals.views import (
    goals_for_period,
    goals_period,
)


urlpatterns = [
    # path('', master_budget_dashboard, name="master_budget_dashboard"),
    path('', goals_for_period, name="goals_for_period"),
    path('goal_period_edit/<int:id>/', goals_period, name="goals-period-edit"),
]
