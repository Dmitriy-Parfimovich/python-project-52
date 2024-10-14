from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


TEST_TASK_PK = '1'
TEST_USER_LOGIN = 'zzzxxx'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'


class TestTaskInfoView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_task_info(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('task_info', kwargs={'pk': TEST_TASK_PK}))
        self.assertTemplateUsed(response, 'tasks/task_info.html')
