import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth.models import User

from .base import AuthBaseTest


@pytest.mark.functional_test
class AuthLoginTest(AuthBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/form'
        )

    def form_field_test_with_callback(self, callback):
        url = reverse('authentication:login')
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

        form.find_element(By.NAME, 'email').send_keys('test@gmail.com')
        form.find_element(By.NAME, 'password').send_keys('Test123')

        callback(form)
        return form

    def test_empty_email_error_message(self):
        def callback(form):
            email_field = form.find_element(By.NAME, 'email')
            email_field.clear()
            email_field.send_keys(' ')
            email_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Campo de email vazio.', message)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = form.find_element(By.NAME, 'email')
            email_field.clear()
            email_field.send_keys('invalid@gmail')
            email_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Email inválido.', message)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            email_field = form.find_element(By.NAME, 'password')
            email_field.clear()
            email_field.send_keys(' ')
            email_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Campo de senha vazio.', message)
        self.form_field_test_with_callback(callback)

    def test_invalid_password_error_message(self):
        def callback(form):
            email_field = form.find_element(By.NAME, 'password')
            email_field.clear()
            email_field.send_keys('invalid')
            email_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Senha inválida.', message)
        self.form_field_test_with_callback(callback)

    def test_login_is_success(self):
        User.objects.create_user(
            username='UserTest',
            password='Test123',
            email='test@gmail.com'
        )

        def callback(form):
            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Login realizado com sucesso.', message)
        self.form_field_test_with_callback(callback)
