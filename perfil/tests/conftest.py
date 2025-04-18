from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client


USERNAME = settings.TEST_USERNAME
PASSWORD = settings.TEST_PASSWORD

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=USERNAME, password=PASSWORD, email="test@email.com"
        )
        self.client.login(
            username=self.user.username, password=PASSWORD
        )
