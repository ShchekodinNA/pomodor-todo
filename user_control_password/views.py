from os import environ
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
from dataclasses import dataclass
# Create your views here.5


@dataclass
class BodyEmailParamsDTO:
    protocol: str
    domain: str
    template_name: str
    subject: str


class PasswordResetView(View):
    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)
        self.password_reset_form = None

    def get(self, request):
        if not self.password_reset_form:
            self.password_reset_form = PasswordResetForm()
        return render(request, 'user_control_password/password_reset.html',
                      context={'reset_form': self.password_reset_form})

    def post(self, request):
        self.password_reset_form = PasswordResetForm(request.POST)
        if self.password_reset_form.is_valid():
            page = self._get_page_and_send_password_reset_email(request)
            return page

    def _get_page_and_send_password_reset_email(self, request: any):
        users_to_reset = self._get_users_by_email_from_form()
        if users_to_reset:
            self._prepare_email_and_send_to_users(users_to_reset, request)

        return redirect('password_reset_done')

    def _get_users_by_email_from_form(self) -> list:
        email = self.password_reset_form.cleaned_data.get('email')
        users_to_reset = list(self.password_reset_form.get_users(email))
        return users_to_reset

    def _prepare_email_and_send_to_users(self, users, request) -> None:
        global_body_params = self._condence_global_body_params_in_dto(request)
        from_mail = environ.get('PUBLIC_EMAIL_ADDRESS')
        for user in users:
            email_body = self._generate_email_body_for(
                user, global_body_params)
            self._send_reset_email(
                global_body_params.subject, email_body, from_mail, user.email)

    def _condence_global_body_params_in_dto(self, request: any) -> BodyEmailParamsDTO:
        body_params = BodyEmailParamsDTO(
            protocol=request.scheme,
            domain=request.get_host(),
            template_name='user_control_password/password_reset_email.txt',
            subject='Password reset'
        )
        return body_params

    def _generate_email_body_for(self, user, body_params: BodyEmailParamsDTO) -> str:
        uid_base_64 = urlsafe_base64_encode(force_bytes(user.pk))
        token_for_user = default_token_generator.make_token(user)
        context_to_body = {
            'uid': uid_base_64,
            'token': token_for_user,
            'domain': body_params.domain,
            'protocol': body_params.protocol,
            'user_login': user.username
        }
        email_body = render_to_string(
            body_params.template_name, context_to_body)
        return email_body

    def _send_reset_email(self, subject: str, body: str, from_mail: str, to_mail: str) -> None:
        try:
            send_mail(subject, body, from_mail,
                      [to_mail], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('invalid header found')