from django.urls import path
from .views import CreateUserAPIView

urlpatterns = [
    path(r'^create/$', CreateUserAPIView.as_view()),
]
