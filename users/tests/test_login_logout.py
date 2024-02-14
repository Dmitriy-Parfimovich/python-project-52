from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'


class TestLoginLogoutView(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_login_logout(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'), username=TEST_USER_LOGIN,
                                    password=TEST_USER_PASSWORD, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
