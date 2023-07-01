from django.test import TestCase, Client
from django.contrib.auth.models import User


class ClientTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

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
