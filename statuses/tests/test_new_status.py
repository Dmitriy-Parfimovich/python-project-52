from django.test import Client, TestCase
from django.urls import reverse
from statuses.forms import NewStatusForm
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'
TEST_STATUS = {'name': 'status3'}
TEST_STATUS_INVALID_FORM = {'name': ''}


class TestNewStatusView(TestCase):

    fixtures = ['statuses.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_new_status_page_template_used_and_status_code(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        # Issue a GET request.
        response = self.client.get(reverse('new_status_create'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the template is OK.
        self.assertTemplateUsed(response, 'statuses/new_status.html')

    def test_create_status(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('new_status_create'), TEST_STATUS,
                                    follow=True)
        self.assertIn('/statuses/', response.redirect_chain[0])


class TestFormNewStatusCreate(TestCase):

    def test_form_new_status_valid(self):
        form = NewStatusForm(data=TEST_STATUS)
        self.assertTrue(form.is_valid())

    def test_form_new_status_invalid(self):
        form = NewStatusForm(data=TEST_STATUS_INVALID_FORM)
        self.assertFalse(form.is_valid())
