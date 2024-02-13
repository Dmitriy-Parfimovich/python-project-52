from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestUserDeleteView(TestCase):
    #Test the methods for the user's edit view.
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
    
    def test_not_authorized_user_to_delete(self):
        user = self.user.objects.get(username='zzzxxx')
        response = self.client.get(self.user.get_absolute_url_delete(user), follow=True)
        self.assertIn('/users/login/', response.redirect_chain[0])
    
    def test_authorized_user_to_delete(self):
        user = self.user.objects.get(username='zzzxxx')
        response = self.client.post(reverse('login'), username='zzzxxx', password='123', follow=True)
        response = self.client.get(self.user.get_absolute_url_delete(user), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_valid_delete_user(self):
        user = self.user.objects.get(username='zzzxxx')
        #response = self.client.post(reverse('login'), {'username': user.username, 'password': user.password}, follow=True)
        print(self.client.login(username=user.username, password=user.password), 'hhhhhhhhhhh')
        #users = self.user.objects.all()
        #print(users, 'xxxxxxxxxxxxxxx')
        #deleted_user = {'first_name': 'zzz', 'last_name': 'xxx',
        #               'username': 'zzzxxx', 'password': '123',
        #               'password2': '123'}
        #print(response, 'kkkkkkkkkkkkkkkkkk')
        self.assertTrue(user.is_authenticated)
        #response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}), follow=True)
        #print(self.client.get(reverse('users_list')), 'kkkkkkkkkkkkkkkkkkk')
        #print(response.redirect_chain, 'ccccccccccccccccc')
        #users = self.user.objects.all()
        #print(users, 'ddddddddddddddddddd')
        #self.assertIn('/users/', response.redirect_chain[0])