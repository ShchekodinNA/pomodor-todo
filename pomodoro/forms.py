from .models import PomodoroSettingToUser
from django.forms import ModelForm, Form

class PomodoroSettingForm(ModelForm):
    class Meta:
        model = PomodoroSettingToUser
        fields = ('id',)
        