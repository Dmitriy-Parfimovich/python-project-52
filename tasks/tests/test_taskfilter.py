from django.test import Client, TestCase
from django.urls import reverse
from tasks.models import Task
from tasks.filters import TaskFilter
from django.contrib.auth import get_user_model


TEST_STATUS = 1
TEST_EXECUTOR = 1
TEST_LABEL = 2
TEST_USER_LOGIN = 'qqqwww'
TEST_USER_PASSWORD = '1q2w3e4r5t6y7'
SELF_TASKS_FLAG_IN_REQUEST = {'self_tasks': ['on']}
TEST_LIST_TASKS_TEST_STATUS = ['task1', 'task3', 'task5']
TEST_LIST_TASKS_TEST_EXECUTOR = ['task1', 'task2', 'task4']
TEST_LIST_TASKS_TEST_LABEL = ['task1', 'task2', 'task3', 'task5']
TEST_LIST_TASKS_TEST_STATUS_EXECUTOR_LABEL = ['task1']
TEST_LIST_TASKS_FOR_VALID_USER = ['task3', 'task4', 'task5']


class TestTasksListView(TestCase):

    fixtures = ['tasks.json']

    def setUp(self):
        # Create a test database.
        # Every test needs a client.
        self.client = Client()
        self.user = get_user_model()
        for user in self.user.objects.all():
            user.set_password(user.password)
            user.save()

    def test_tasks_list_page_template_used_and_task_code(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        # Issue a GET request.
        response = self.client.get(reverse('tasks_list'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the template is OK.
        self.assertTemplateUsed(response, 'tasks/tasks.html')

    def test_taskfilter_test_form_and_status(self):
        tasks = Task.objects.all()
        form = TaskFilter(data={'status': TEST_STATUS}, queryset=tasks)
        self.assertTrue(form.is_valid())
        result = form.qs.order_by('pk')
        result = [result.name for result in result]
        self.assertEqual(result, TEST_LIST_TASKS_TEST_STATUS)

    def test_taskfilter_test_form_and_executor(self):
        tasks = Task.objects.all()
        form = TaskFilter(data={'executor': TEST_EXECUTOR}, queryset=tasks)
        self.assertTrue(form.is_valid())
        result = form.qs.order_by('pk')
        result = [result.name for result in result]
        self.assertEqual(result, TEST_LIST_TASKS_TEST_EXECUTOR)

    def test_taskfilter_test_form_and_label(self):
        tasks = Task.objects.all()
        form = TaskFilter(data={'labels': TEST_LABEL}, queryset=tasks)
        self.assertTrue(form.is_valid())
        result = form.qs.order_by('pk')
        result = [result.name for result in result]
        self.assertEqual(result, TEST_LIST_TASKS_TEST_LABEL)

    def test_taskfilter_test_form_and_status_executor_label(self):
        tasks = Task.objects.all()
        form = TaskFilter(data={'status': TEST_STATUS, 'executor': TEST_EXECUTOR,
                                'labels': TEST_LABEL}, queryset=tasks)
        self.assertTrue(form.is_valid())
        result = form.qs.order_by('pk')
        result = [result.name for result in result]
        self.assertEqual(result, TEST_LIST_TASKS_TEST_STATUS_EXECUTOR_LABEL)

    def test_tasklist_for_valid_user(self):
        response = self.client.login(username=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('tasks_list'), data=SELF_TASKS_FLAG_IN_REQUEST)
        self.assertEqual(response.status_code, 200)
        result = response.context['tasks'].order_by('pk')
        result = [result.name for result in result]
        self.assertEqual(result, TEST_LIST_TASKS_FOR_VALID_USER)
