from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


TEST_USER_LOGIN_1 = 'zzzxxx'
TEST_USER_LOGIN_2 = 'dddfff'
TEST_USER_PASSWORD = '123'
TEST_USER_PK = 1


class TestUserDeleteView(TestCase):
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

    def test_not_authorized_user_to_delete(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN_1)
        response = self.client.get(self.user.get_absolute_url_delete(user), follow=True)
        self.assertIn('/users/login/', response.redirect_chain[0])

    def test_authorized_user_to_delete(self):
        user = self.user.objects.get(username=TEST_USER_LOGIN_1)
        response = self.client.post(reverse('login'), username=TEST_USER_LOGIN_1,
                                    password=TEST_USER_PASSWORD, follow=True)
        response = self.client.get(self.user.get_absolute_url_delete(user), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_user(self):
        self.client.login(username=TEST_USER_LOGIN_1, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('user_delete', kwargs={'pk': TEST_USER_PK}),
                                    follow=True)
        self.assertIn('/users/', response.redirect_chain[0])

    def test_invalid_delete_user(self):
        self.client.login(username=TEST_USER_LOGIN_1, password=TEST_USER_PASSWORD)
        user = self.user.objects.get(username=TEST_USER_LOGIN_2)
        response = self.client.get(self.user.get_absolute_url_delete(user), follow=True)
        self.assertIn('/users/', response.redirect_chain[0])
