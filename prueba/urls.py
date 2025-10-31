from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestErrorView


urlpatterns = [
    path("api/test-error/", TestErrorView.as_view(), name="test-error")
]
