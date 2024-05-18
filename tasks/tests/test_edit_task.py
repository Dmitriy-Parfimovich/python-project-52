from django.test import Client, TestCase
from tasks.models import Task


TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'

TEST_TASK = 'task1'

TEST_VALID_TASK = {'taskname': 'taskname111', 'executor': 1, 'status': 1}


class TestTaskEditView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.task = Task

    def test_authorized_user_to_edit_task(self):
        task = self.task.objects.get(taskname=TEST_TASK)
        response = self.client.get(self.task.get_absolute_url_edit(task), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_task_edit(self):
        task = self.task.objects.get(taskname=TEST_TASK)
        response = self.client.post(self.task.get_absolute_url_edit(task),
                                    TEST_VALID_TASK, follow=True)
        self.assertIn('/tasks/', response.redirect_chain[0])
