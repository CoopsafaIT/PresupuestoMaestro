from django.urls import path
from apps.goals.views import (
    goals_for_period,
    add_goals_period,
)


urlpatterns = [
    # path('', master_budget_dashboard, name="master_budget_dashboard"),
    path('', goals_for_period, name="goals_for_period"),
    path('add_goals_period/', add_goals_period, name="add-goals-period"),
    path('add_goals_period/<int:id>/', add_goals_period, name="edit-goals-period"),
]
