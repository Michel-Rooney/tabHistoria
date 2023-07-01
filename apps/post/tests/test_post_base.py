from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.post.models import Post, Comment


class PostTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_client(
        self,
        username='Test user',
        password='Test123',
        email='testemail@gmail.com'
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email)

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

    def make_post(
        self,
        title='Title',
        creator=None,
        content='Content',
    ):
        if creator is None:
            creator = {}

        return Post.objects.create(
            title=title,
            creator=self.make_client(),
            content=content
        )

    def make_comment(
        self,
        creator=None,
        content='Content',
    ):
        if creator is None:
            creator = {}

        return Comment.objects.create(
            creator=self.make_client(),
            content=content,
        )
