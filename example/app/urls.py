from app.views import ExampleView
from django.urls import path

urlpatterns = [
    path("", ExampleView.as_view()),
]
