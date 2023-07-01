from django.contrib import messages
from django.urls import resolve, reverse
from .. import views
from parameterized import parameterized
from .test_client_base import ClientTestBase


class ClientViewsTest(ClientTestBase):
    @parameterized.expand([
        ('client:profile', views.profile),
        ('client:update_profile', views.update_profile)
    ])
    def test_client_view_function_is_correct(self, path_name, correct_view):
        view = resolve(reverse(path_name, kwargs={'id': 1}))
        self.assertIs(view.func, correct_view)

    @parameterized.expand([
        ('client:profile'),
        ('client:update_profile')
    ])
    def test_client_view_returns_status_code_200_OK(self, path_name):
        client = self.make_login_client()
        response = client.get(reverse(path_name, kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('client:profile', 'pages/profile.html'),
        ('client:update_profile', 'pages/update_profile.html')
    ])
    def test_client_view_loads_correct_template(self, path_name, correct_template):
        client = self.make_login_client()
        response = client.get(reverse(path_name, kwargs={'id': 1}))
        self.assertTemplateUsed(response, correct_template)

    @parameterized.expand([
        ('client:profile'),
        ('client:update_profile')
    ])
    def test_client_invalid_request(self, path_name):
        client = self.make_login_client()
        url = reverse(path_name, kwargs={'id': 1})
        response = client.put(url)
        message = response.content.decode('utf-8')
        self.assertEqual(message, "Invalid request")

    def test_client_update_not_have_access_permission(self):
        self.make_login_client()
        client_request = self.make_login_client(
            username='Request', password='Request123',
            email='request@gmail.com'
        )
        url = reverse('client:update_profile', kwargs={'id': 1})
        response = client_request.get(url)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Você não tem permissão de acesso.')
        self.assertEqual(response.url, '/client/profile/2/')

    def test_client_update_email_validation_error(self):
        client = self.make_login_client()
        data = {
            'username': 'Test email validation error',
            'email': 'invalid email'
            }
        url = reverse('client:update_profile', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Email inválido.')

    def test_client_update_is_success(self):
        client = self.make_login_client()
        data = {
            'username': 'New username',
            'email': 'newemail@gmail.com'
        }
        url = reverse('client:update_profile', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Usuário atualizado com sucesso')
        self.assertEqual(response.url, '/client/update_profile/1/')
