from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task


TEST_TASK = 'task2'
TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '123'
TEST_TASK_VALID_PK = 2
TEST_TASK_INVALID_PK = 1


class TestTaskDeleteView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        self.task = Task
        # Fix the passwords of fixtures
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_authorized_user_to_delete_task(self):
        task = self.task.objects.get(taskname=TEST_TASK)
        response = self.client.get(self.task.get_absolute_url_delete(task), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_user_get(self):
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('task_delete', kwargs={'pk': TEST_TASK_VALID_PK}))
        self.assertTemplateUsed(response, 'tasks/del_task.html')

    def test_valid_delete_user_post(self):
        response = self.client.post(reverse('task_delete', kwargs={'pk': TEST_TASK_VALID_PK}),
                                    follow=True)
        self.assertIn('/tasks/', response.redirect_chain[0])

    def test_invalid_delete_user_get(self):
        self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('task_delete', kwargs={'pk': TEST_TASK_INVALID_PK}),
                                    follow=True)
        self.assertIn('/tasks/', response.redirect_chain[0])
