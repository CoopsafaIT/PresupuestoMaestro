from django.urls import path
from apps.main.views import (
    dashboard,
)

urlpatterns = [
    path('', dashboard, name="dashboard"),
]
