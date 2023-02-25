from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register_request, name='register_user'),
    path('login', views.login_request, name='login_user'),
    path('logout', views.logout_request, name='logout_user')
]
