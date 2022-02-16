from django.urls import path
from apps.master_budget.views import (
    master_budget_dashboard,
    projection_parameters,
    projection_parameter,
    profit_loss_report_complementary_projection,
    profit_loss_report_complementary_projection_detail
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
    path(
        'profit-and-loss-reports/complementary-projection-list',
        profit_loss_report_complementary_projection,
        name="profit_loss_report_complementary_projection"
    ),
    path(
        'profit-and-loss-reports/complementary-projection-detail/<int:period_id>/',
        profit_loss_report_complementary_projection_detail,
        name="profit_loss_report_complementary_projection_detail"
    ),
]
