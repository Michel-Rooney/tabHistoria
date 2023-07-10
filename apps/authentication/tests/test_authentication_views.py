from django.urls import reverse, resolve
from .. import views
from .test_authentication_base import AuthenticationTestBase
from parameterized import parameterized
from django.test import Client
from django.contrib import messages


class AuthenticationViewsTest(AuthenticationTestBase):
    @parameterized.expand([
            ('authentication:register', views.register),
            ('authentication:login', views.login),
            ('authentication:logout', views.logout),
        ])
    def test_authentication_view_function_is_correct(self, path_name, correct_view):  # noqa: E501
        view = resolve(reverse(path_name))
        self.assertIs(view.func, correct_view)

    @parameterized.expand([
            ('authentication:register', 200),
            ('authentication:login', 200),
            ('authentication:logout', 302, True),
        ])
    def test_authentication_view_returns_status_code_expect(self, path_name, code, make_client=False):  # noqa: E501
        if make_client:
            self.make_login_logout_client()
        response = self.client.get(reverse(path_name))
        self.assertEqual(response.status_code, code)

    @parameterized.expand([
            ('authentication:register', 'pages/register.html'),
            ('authentication:login', 'pages/login.html'),
        ])
    def test_authentication_view_loads_correct_template(self, path_name, correct_template):  # noqa: E501
        response = self.client.get(reverse(path_name))
        self.assertTemplateUsed(response, correct_template)

    def test_authentication_logout_view_redirect_correct_with_method_get(self):
        response = self.make_login_logout_client()
        self.assertEqual(response.url, '/')

    @parameterized.expand([
            ('authentication:register'),
            ('authentication:login'),
        ])
    def test_authentication_user_is_authenticated(self, path_name):
        """Testing if the user is barred if he is already logged in"""
        client = self.make_login_client()
        request = client.get(reverse(path_name))
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, '/')

    @parameterized.expand([
        ('authentication:register'),
        ('authentication:login'),
    ])
    def test_authentication_login_email_validation_error(self, path_name):
        client = self.make_login_client()
        data = {
            'username': 'Test email validation error',
            'email': 'invalid email'
            }
        response = client.post(reverse(path_name), data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(stored_messages[0].message, 'Email inválido.')

    def test_authentication_new_register_is_success(self):
        client = Client()
        url = reverse('authentication:register')
        data = {
            'username': 'Test user',
            'email': 'testemail@gmail.com',
            'password': 'Test123'
        }
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Usuário criado com sucesso.')

    def test_authentication_login_is_success(self):
        client = self.make_login_client()
        url = reverse('authentication:login')
        data = {
            'username': 'Test user',
            'email': 'testemail@gmail.com',
            'password': 'Test123'
        }
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Login realizado com sucesso.')
        self.assertEqual(response.url, '/')

    def test_authentication_login_is_fail(self):
        client = self.make_login_client()
        url = reverse('authentication:login')
        data = {
            'username': 'Test user',
            'email': 'testemail@gmail.com',
            'password': 'Test1234'
        }
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Falha no login.')
        self.assertEqual(response.url, '/auth/login/')

    @parameterized.expand([
        ('authentication:register', 'Invalid request'),
        ('authentication:login', 'Invalid request'),
        ('authentication:logout', 'Requisição de logout inválida.')
    ])
    def test_authentication_invalid_request(self, path_name, message_correct):
        client = self.make_login_client()
        url = reverse(path_name)
        response = client.put(url, follow=True)
        message = response.content.decode('utf-8')
        self.assertIn(message_correct, message)
