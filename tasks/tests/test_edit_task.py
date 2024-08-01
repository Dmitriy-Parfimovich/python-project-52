from django.test import Client, TestCase
from tasks.models import Task
from django.contrib.auth import get_user_model


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'

TEST_TASK = 'task1'

TEST_VALID_TASK = {'name': 'taskname111', 'executor': 1, 'status': 1, 'labels': [1, 2, 3]}


class TestTaskEditView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.task = Task
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_authorized_user_to_edit_task(self):
        task = self.task.objects.get(name=TEST_TASK)
        response = self.client.get(self.task.get_absolute_url_edit(task), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_task_edit(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        task = self.task.objects.get(name=TEST_TASK)
        response = self.client.post(self.task.get_absolute_url_edit(task),
                                    TEST_VALID_TASK, follow=True)
        self.assertIn('/tasks/', response.redirect_chain[0])
