from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "to_do_pomodoro.settings")
setup()
from django.test import TestCase, Client
from django.urls import reverse
from pomodoro.models import PomodoroSettingToUser
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.pomodoro_settings_url = reverse('pomodoro-settings')
        self.user1_login = 'Test1'
        self.user1_password = 'some_hash'
        self.user1 = User.objects.create_user( self.user1_login , 'email@test.com', self.user1_password )
    
    def test_settings_with_existing_GET(self):
        self.client.login(username=self.user1_login, password=self.user1_password)
        setting1_id = PomodoroSettingToUser.objects.create(
            user=self.user1,
            active=True
        ).pk
        response = self.client.get(self.pomodoro_settings_url)
        
        self.assertEqual(response.status_code, 200)
    
    def test_settings_without_existing_GET(self):
        response = self.client.get(self.pomodoro_settings_url)
        
        self.assertEqual(response.status_code, 403)