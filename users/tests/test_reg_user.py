from django.test import Client, TestCase
from django.urls import reverse
from users.forms import UserRegForm
from django.contrib.auth import get_user_model


class TestNewUserRegView(TestCase):
    #Test the methods for the user's registartion view.
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
        response = self.client.post(reverse('new_user_reg'), {'first_name': 'qqq',
                                                              'last_name': 'www',
                                                              'username': 'qqqwww',
                                                              'password': '123',
                                                              'password2': '123'},
                                                              follow=True)
        self.assertIn('/users/login/', response.redirect_chain[0])
    
    def test_create_invalid_user(self):
        response = self.client.post(reverse('new_user_reg'), {'first_name': 'qqq',
                                                              'last_name': 'www',
                                                              'username': '////',
                                                              'password': '123',
                                                              'password2': '123'})
        self.assertEqual(response.status_code, 200)


class TestFormNewUserReg(TestCase):

    def test_form_new_user_reg_valid(self):
        form_data = {'first_name': 'aaa', 'last_name': 'sss',
                     'username': 'aaasss', 'password': '123',
                     'password2': '123'}
        form = UserRegForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_new_user_reg_invalid_1(self):
        form_data = {'first_name': 'aaa', 'last_name': 'sss',
                     'username': 'aaasss', 'password': '123',
                     'password2': '321'}
        form = UserRegForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_new_user_reg_invalid_2(self):
        form_data = {'first_name': 'aaa', 'last_name': 'sss',
                     'username': 'aaasss', 'password': '12',
                     'password2': '12'}
        form = UserRegForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_new_user_reg_invalid_3(self):
        form_data = {'first_name': 'aaa', 'last_name': 'sss',
                     'username': '~~~', 'password': '12',
                     'password2': '12'}
        form = UserRegForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_new_user_reg_invalid_4(self):
        form_data = {'first_name': 'zzz', 'last_name': 'xxx',
                     'username': 'zzzxxx', 'password': '12',
                     'password2': '12'}
        form = UserRegForm(data=form_data)
        self.assertFalse(form.is_valid())