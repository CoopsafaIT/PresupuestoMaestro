from django.urls import path

from . import views

urlpatterns = [
    path('scenarios/', views.scenarios_equity, name="scenarios_equity"),
    path('scenario/detail/<int:id>/', views.scenario_equity, name="scenario_equity")
]
