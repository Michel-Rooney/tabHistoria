from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_login_logout_client(
        self,
        username='Test user',
        password='Test123',
    ):
        # Crie um cliente de teste
        client = Client()

        # Crie um usuário de teste
        User.objects.create_user(username=username, password=password)

        # Faça login com o usuário de teste
        logged_in = client.login(username=username, password=password)
        self.assertTrue(logged_in)  # Verifica se o login foi bem-sucedido

        # Faça uma solicitação GET para a visualização de logout
        response = client.get(reverse('authentication:logout'))
        return response

    def make_login_client(
        self,
        username='Test user',
        password='Test123',
        email='testemail@gmail.com'
    ):
        # Crie um cliente de teste
        client = Client()

        # Crie um usuário de teste
        User.objects.create_user(
            username=username,
            password=password,
            email=email)

        # Faça login com o usuário de teste
        logged_in = client.login(username=username, password=password)
        self.assertTrue(logged_in)  # Verifica se o login foi bem-sucedido
        return client
