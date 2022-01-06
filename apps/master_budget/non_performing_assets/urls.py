from django.urls import path
from . import views

urlpatterns = [
    path(
        'non-performing-assets/scenarios/',
        views.scenarios_non_performing_assets,
        name="scenarios_non_performing_assets"
    ),
    path(
        'non-performing-assets/scenario/detail/<int:id>/',
        views.scenario_non_performing_assets,
        name="scenario_non_performing_assets"
    ),

    path(
        'others-assets/scenarios/',
        views.scenarios_others_assets,
        name="scenarios_others_assets"
    ),
    path(
        'others-assets/scenario/detail/<int:id>/',
        views.scenario_others_assets,
        name="scenario_others_assets"
    ),
]
