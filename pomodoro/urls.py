from django.urls import path
from .views import SettingView
urlpatterns = [
    path('settings', SettingView.as_view(), name='pomodoro-settings')
]