from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model



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
        user = self.user.objects.get(username='zzzxxx')
        response = self.client.post(reverse('login'), username='zzzxxx', password='123', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
