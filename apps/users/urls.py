from django.urls import path
from .views import RegisterView, LogoutView


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/logout/", LogoutView.as_view()),
]
