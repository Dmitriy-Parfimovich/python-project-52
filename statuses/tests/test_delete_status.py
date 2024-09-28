from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status


TEST_STATUS = 'status2'
TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'
TEST_STATUS_PK = 2


class TestStatusDeleteView(TestCase):

    fixtures = ['statuses.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        self.status = Status
        # Fix the passwords of fixtures
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_authorized_user_to_delete_status(self):
        status = self.status.objects.get(name=TEST_STATUS)
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('status_delete', args=[status.id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_user(self):
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('status_delete', kwargs={'pk': TEST_STATUS_PK}),
                                    follow=True)
        self.assertIn('/statuses/', response.redirect_chain[0])
