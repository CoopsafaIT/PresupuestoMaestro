from django.urls import path
from apps.goals.views import (
    goals,
    goals_for_period,
    goals_period,
    goals_detail
)


urlpatterns = [
    path('', goals, name="goals"),
    path('goal-period-list/', goals_for_period, name="goals_for_period"),
    path('goal-period-edit/<int:id>/', goals_period, name="goals_period_edit"),
    path('goal-detail/', goals_detail, name="goals_detail"),
]
