from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .forms import PomodoroSettingForm
from .models import PomodoroSettingToUser

from django.http import HttpResponse

# Create your views here.


class SettingView(View):
    def get(self, request):
        try:
            settings_of_current_user = PomodoroSettingToUser.objects.filter(
                user=self.request.user)
        except TypeError:
            return HttpResponse(status=403)
        settings = []

        for setting in settings_of_current_user:
            settings.append(setting.__dict__)

        return render(request, 'pomodoro/settings.html', context={
            'settings': settings
        })

    def post(self, request):
        innter_method: str = request.POST.get('inner_method', None)
        setting_id: int = int(request.POST.get('setting_id', 0))
        if not innter_method or not setting_id:
            return HttpResponse(status=403)
        match innter_method.lower():
            case 'delete':
                self._delete_request(request, setting_id)
            case 'activate':
                self._activate_setting(request, setting_id)
        return self.get(request)

    def _delete_request(self, request: any, setting_id: int):
        setting_to_delete: PomodoroSettingToUser = PomodoroSettingToUser.objects.filter(
            pk=setting_id, user=self.request.user).first()
        if setting_to_delete:
            setting_to_delete.delete()
    
    def _activate_setting(self, request: any, setting_id: int):
        setting_to_activate: PomodoroSettingToUser = PomodoroSettingToUser.objects.filter(
            pk=setting_id, user=self.request.user).first()
        if setting_to_activate:
            setting_to_activate.active = True
            setting_to_activate.save()

class SettingDetailView(View):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_form = None
    
    def get(self, request, id):
        if not self.settings_form:
            self.settings_form = PomodoroSettingForm
        return render(request, 'pomodoro/setting_detail.html', context={'setting_form': self.settings_form})
    
    