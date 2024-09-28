from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'

TEST_VALID_USER = {'first_name': 'zzz', 'last_name': 'xxx',
                   'username': 'mmmmmm', 'password1': '1q2w3e4r5t6y7',
                   'password2': '1q2w3e4r5t6y7'}
TEST_INVALID_USER = {'first_name': 'zzz', 'last_name': 'xxx',
                     'username': '//////', 'password1': '1q2w3e4r5t6y7',
                     'password2': '1q2w3e4r5t6y7'}


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
        response = self.client.get(reverse('user_edit', args=[user.id]), follow=True)
        self.assertIn('/login/', response.redirect_chain[0])

    def test_authorized_user_to_edit(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('user_edit', args=[user.id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_user(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('user_edit', args=[user.id]),
                                    TEST_VALID_USER, follow=True)
        self.assertIn('/users/', response.redirect_chain[0])

    def test_invalid_edit_user(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN)
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('user_edit', args=[user.id]),
                                    TEST_INVALID_USER, follow=True)
        self.assertEqual(response.status_code, 200)
