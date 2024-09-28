from django.test import Client, TestCase
from django.urls import reverse
from users.forms import UserRegForm
from django.contrib.auth import get_user_model


TEST_VALID_USER = {'first_name': 'qqq', 'last_name': 'www',
                   'username': 'qqqwww', 'password1': '1q2w3e4r5t6y7',
                   'password2': '1q2w3e4r5t6y7'}
TEST_INVALID_USER = {'first_name': 'qqq', 'last_name': 'www',
                     'username': '////', 'password1': '1q2w3e4r5t6y7',
                     'password2': '1q2w3e4r5t6y7'}
TEST_VALID_FORM_DATA = {'first_name': 'aaa', 'last_name': 'sss',
                        'username': 'aaasss', 'password1': '1q2w3e4r5t6y7',
                        'password2': '1q2w3e4r5t6y7'}
TEST_INVALID_FORM_DATA_1 = {'first_name': 'aaa', 'last_name': 'sss',
                            'username': 'aaasss', 'password1': '1q2w3e4r5t6y7',
                            'password2': '7y6t5r4e3w2q1'}
TEST_INVALID_FORM_DATA_2 = {'first_name': 'aaa', 'last_name': 'sss',
                            'username': 'aaasss', 'password1': '12',
                            'password2': '12'}
TEST_INVALID_FORM_DATA_3 = {'first_name': 'aaa', 'last_name': 'sss',
                            'username': '~~~', 'password1': '12',
                            'password2': '12'}
TEST_INVALID_FORM_DATA_4 = {'first_name': 'zzz', 'last_name': 'xxx',
                            'username': 'zzzxxx', 'password1': '12',
                            'password2': '12'}


class TestNewUserRegView(TestCase):
    # Test the methods for the user's registartion view.
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

    def test_reg_page_template_used_and_status_code(self):
        # Issue a GET request.
        response = self.client.get(reverse('new_user_reg'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the template is OK.
        self.assertTemplateUsed(response, 'users/reg.html')

    def test_create_valid_user(self):
        response = self.client.post(reverse('new_user_reg'), TEST_VALID_USER,
                                    follow=True)
        self.assertIn('/login/', response.redirect_chain[0])

    def test_create_invalid_user(self):
        response = self.client.post(reverse('new_user_reg'), TEST_INVALID_USER)
        self.assertEqual(response.status_code, 200)


class TestFormNewUserReg(TestCase):

    def test_form_new_user_reg_valid(self):
        form = UserRegForm(data=TEST_VALID_FORM_DATA)
        self.assertTrue(form.is_valid())

    def test_form_new_user_reg_invalid_1(self):
        form = UserRegForm(data=TEST_INVALID_FORM_DATA_1)
        self.assertFalse(form.is_valid())

    def test_form_new_user_reg_invalid_2(self):
        form = UserRegForm(data=TEST_INVALID_FORM_DATA_2)
        self.assertFalse(form.is_valid())

    def test_form_new_user_reg_invalid_3(self):
        form = UserRegForm(data=TEST_INVALID_FORM_DATA_3)
        self.assertFalse(form.is_valid())

    def test_form_new_user_reg_invalid_4(self):
        form = UserRegForm(data=TEST_INVALID_FORM_DATA_4)
        self.assertFalse(form.is_valid())
