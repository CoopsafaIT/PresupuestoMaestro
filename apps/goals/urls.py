from django.urls import path
from apps.goals.views import (
    goals_dashboard,
    global_goals_period,
    goals_period_edit,
    goals_global_definition,
    goals,
    goal_edit
)


urlpatterns = [
    path('dashboard/', goals_dashboard, name="goals_dashboard"),
    path('global/period/', global_goals_period, name="global_goals_period"),
    path('period/edit/<int:id>/', goals_period_edit, name="goals_period_edit"),
    path(
        'global/definition/<str:id_global_goal_period>/',
        goals_global_definition,
        name="goals_global_definition"
    ),
    path('goals/list/', goals, name="goals"),
    path('goal/edits/<int:id>/', goal_edit, name="goal_edit")
]
