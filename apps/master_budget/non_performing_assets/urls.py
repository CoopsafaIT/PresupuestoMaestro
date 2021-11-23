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
        'non-performing-assets/scenario/detail/comments/<int:id>/',
        views.scenario_non_performing_assets_comments,
        name="scenario_non_performing_assets_comments"
    ),
]
