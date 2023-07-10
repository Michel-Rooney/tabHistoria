from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthLogoutTest(TestCase):
    def login_client(self):
        username = 'TestUser'
        password = 'Pass'

        User.objects.create_user(
            username=username,
            password=password,
        )

        self.client.login(
            username=username,
            password=password
        )

    def test_user_tries_to_logout_using_get_method(self):
        self.login_client()

        response = self.client.get(
            reverse('authentication:logout'),
            follow=True
        )

        self.assertIn(
            'Requisição de logout inválida.',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        self.login_client()

        response = self.client.post(
            reverse('authentication:logout'),
            data={'username': 'another_user'},
            follow=True
        )

        self.assertIn(
            'User logout inválido.',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authentication:logout'),
            data={
                'username': 'my_user'
            },
            follow=True
        )

        self.assertIn(
            'Logout realizado com sucesso.',
            response.content.decode('utf-8')
        )
