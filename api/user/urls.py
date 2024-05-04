from django.urls import path
from .views import LoginApiView,RegisterApiView

urlpatterns = [
    path("login",view=LoginApiView.as_view(),name="login"),
    path("register",view=RegisterApiView.as_view(),name="register")
]
