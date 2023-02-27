from django.contrib import admin
from .models import PomodoroSettingToUser
# Register your models here.


class PomodoroSettingToUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PomodoroSettingToUser._meta.fields]

admin.site.register(PomodoroSettingToUser, PomodoroSettingToUserAdmin)