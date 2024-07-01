from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from statuses.models import Status


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'

TEST_STATUS = 'status1'

TEST_VALID_STATUS = {'name': 'status3'}


class TestStatusEditView(TestCase):

    fixtures = ['statuses.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        self.status = Status
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_authorized_user_to_edit_status(self):
        status = self.status.objects.get(name=TEST_STATUS)
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(self.status.get_absolute_url_edit(status), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_status_edit(self):
        status = self.status.objects.get(name=TEST_STATUS)
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(self.status.get_absolute_url_edit(status),
                                    TEST_VALID_STATUS, follow=True)
        self.assertIn('/statuses/', response.redirect_chain[0])
