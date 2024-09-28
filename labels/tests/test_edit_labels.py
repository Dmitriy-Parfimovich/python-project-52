from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from labels.models import Label
from django.urls import reverse


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'

TEST_LABEL = 'label1'

TEST_VALID_LABEL = {'name': 'label3'}


class TestLabelEditView(TestCase):

    fixtures = ['labels.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        self.label = Label
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_authorized_user_to_edit_label(self):
        label = self.label.objects.get(name=TEST_LABEL)
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('label_edit', args=[label.id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_label_edit(self):
        label = self.label.objects.get(name=TEST_LABEL)
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('label_edit', args=[label.id]),
                                    TEST_VALID_LABEL, follow=True)
        self.assertIn('/labels/', response.redirect_chain[0])
