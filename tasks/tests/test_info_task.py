from django.test import Client, TestCase
from django.urls import reverse


TEST_TASK_PK = '1'


class TestTaskInfoView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()

    def test_task_info(self):
        response = self.client.get(reverse('task_info', kwargs={'pk': TEST_TASK_PK}))
        self.assertTemplateUsed(response, 'tasks/task_info.html')
