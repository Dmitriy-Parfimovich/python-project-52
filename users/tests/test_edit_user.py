from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'

TEST_VALID_USER = {'first_name': 'zzz', 'last_name': 'xxx',
                   'username': 'mmmmmm', 'password1': '123',
                   'password2': '123'}
TEST_INVALID_USER = {'first_name': 'zzz', 'last_name': 'xxx',
                     'username': '//////', 'password1': '123',
                     'password2': '123'}


class TestUserEditView(TestCase):
    # Test the methods for the user's edit view.
    fixtures = ['users.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        # Fix the passwords of fixtures
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_not_authorized_user_to_edit(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.get(self.user.get_absolute_url_edit(user), follow=True)
        self.assertIn('/login/', response.redirect_chain[0])

    def test_authorized_user_to_edit(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(self.user.get_absolute_url_edit(user), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_user(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(self.user.get_absolute_url_edit(user),
                                    TEST_VALID_USER, follow=True)
        self.assertIn('/users/', response.redirect_chain[0])

    def test_invalid_edit_user(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(self.user.get_absolute_url_edit(user),
                                    TEST_INVALID_USER, follow=True)
        self.assertEqual(response.status_code, 200)
