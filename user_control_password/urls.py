from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reset/request_sent',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user_control_password/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='user_control_password/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name='user_control_password/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('reset/request',
         views.PasswordResetView.as_view(), name='password_reset')
]
