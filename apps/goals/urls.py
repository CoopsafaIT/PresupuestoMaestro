from django.urls import path
from apps.goals.views import (
    goals_for_period,
    goals_period,
)


urlpatterns = [
    path('', goals_for_period, name="goals_for_period"),
    path('goal-period-edit/<int:id>/', goals_period, name="goals_period_edit"),
]
