from django.test import TestCase
from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "to_do_pomodoro.settings")
setup()
from pomodoro.models import PomodoroSettingToUser
from django.contrib.auth.models import User

class TestModel(TestCase):
    def setUp(self) -> None:
        pass
    
    def test_correct_status_switching(self):
        user1 = User.objects.create_user(
            'Test1', 'test@test.com', 'some_hash'
        )
        setting1_id = PomodoroSettingToUser.objects.create(
            user=user1,
            active=True
        ).pk
        setting2_id = PomodoroSettingToUser.objects.create(
            user=user1,
            active=True
        ).pk
        setting1 = PomodoroSettingToUser.objects.get(id=setting1_id)
        setting2 = PomodoroSettingToUser.objects.get(id=setting2_id)
        self.assertFalse(setting1.active)
        self.assertTrue(setting2.active)