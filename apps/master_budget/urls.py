from django.urls import path
from apps.master_budget.views import (
    master_budget_dashboard,
    projection_parameters,
    projection_parameter
)

urlpatterns = [
    path('', master_budget_dashboard, name="master_budget_dashboard"),
    path(
        'projection-parameters-list/',
        projection_parameters,
        name="projection_parameters"
    ),
    path(
        'projection-parameter-edit/<int:id>/',
        projection_parameter,
        name="projection_parameter"
    ),
]
