from django.urls import path
from . import views

urlpatterns = [
    path(
        'scenarios/',
        views.scenarios_payment_payroll,
        name="scenarios_payment_payroll"
    ),
    path(
        'scenario/detail/<int:id>/',
        views.scenario_payment_payroll,
        name="scenario_payment_payroll"
    ),
]
