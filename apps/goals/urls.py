from django.urls import path
from apps.goals.views import (
    goals_dashboard,
    goals_for_period,
    goals_period,
    goals_global_definition,
    goals,
    goal
)


urlpatterns = [
    path('', goals_dashboard, name="goals_dashboard"),
    path('goal-period-list/', goals_for_period, name="goals_for_period"),
    path('goal-period-edit/<int:id>/', goals_period, name="goals_period_edit"),
    path(
        'goals-global-definition/<str:id_global_goal_period>/',
        goals_global_definition,
        name="goals_global_definition"
    ),
    path('goals-list/', goals, name="goals"),
    path('goal/<int:id>/', goal, name="goal")
]
