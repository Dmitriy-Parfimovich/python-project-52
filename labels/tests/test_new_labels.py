from django.test import Client, TestCase
from django.urls import reverse
from labels.forms import NewLabelForm
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'
TEST_LABEL = {'name': 'label3'}
TEST_LABEL_INVALID_FORM = {'name': ''}


class TestNewLabelView(TestCase):

    fixtures = ['labels.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_new_label_page_template_used_and_status_code(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        # Issue a GET request.
        response = self.client.get(reverse('new_label_create'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the template is OK.
        self.assertTemplateUsed(response, 'labels/create_label.html')

    def test_create_label(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('new_label_create'), TEST_LABEL,
                                    follow=True)
        self.assertIn('/labels/', response.redirect_chain[0])


class TestFormNewLabelCreate(TestCase):

    def test_form_new_label_valid(self):
        form = NewLabelForm(data=TEST_LABEL)
        self.assertTrue(form.is_valid())

    def test_form_new_label_invalid(self):
        form = NewLabelForm(data=TEST_LABEL_INVALID_FORM)
        self.assertFalse(form.is_valid())
