from django.test import Client, TestCase
from django.urls import reverse
from tasks.forms import NewTaskForm
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'
TEST_TASK = {'name': 'taskname111', 'executor': 1, 'status': 1, 'labels': [3]}
TEST_TASK_VALID_FORM = {'name': 'taskname333', 'status': 1, 'labels': [1, 3]}
TEST_TASK_INVALID_FORM1 = {'name': 'taskname222', 'executor': '1', 'status': ''}
TEST_TASK_INVALID_FORM2 = {'name': 'taskname333'}


class TestNewTaskView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_new_task_page_template_used_and_task_code(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        # Issue a GET request.
        response = self.client.get(reverse('new_task_create'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the template is OK.
        self.assertTemplateUsed(response, 'tasks/new_task.html')

    def test_create_task(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('new_task_create'), TEST_TASK, follow=True)
        self.assertIn('/tasks/', response.redirect_chain[0])


class TestFormNewTaskCreate(TestCase):

    fixtures = ['tasks.json']

    def test_form_new_task_valid1(self):
        form = NewTaskForm(data=TEST_TASK)
        self.assertTrue(form.is_valid())

    def test_form_new_task_valid2(self):
        form = NewTaskForm(data=TEST_TASK_VALID_FORM)
        self.assertTrue(form.is_valid())

    def test_form_new_task_invalid1(self):
        form = NewTaskForm(data=TEST_TASK_INVALID_FORM1)
        self.assertFalse(form.is_valid())

    def test_form_new_task_invalid2(self):
        form = NewTaskForm(data=TEST_TASK_INVALID_FORM2)
        self.assertFalse(form.is_valid())
