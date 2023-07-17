from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterAPIView.as_view(), name="core-register"),
    path("login", views.LoginAPIView.as_view(), name="core-login"),
    path("user", views.UserAPIView.as_view(), name="core-user"),
    path("refresh", views.RefreshAPIView.as_view(), name='core-refresh'),
    path("logout", views.LogoutAPIView.as_view(), name='core-logout'),
]
