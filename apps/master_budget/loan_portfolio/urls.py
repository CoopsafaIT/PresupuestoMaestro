from django.urls import path
from .views import scenarios

urlpatterns = [
    path('scenarios/', scenarios, name="scenarios"),
]
