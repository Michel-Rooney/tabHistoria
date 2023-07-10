import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth.models import User

from .base import AuthBaseTest


@pytest.mark.functional_test
class AuthRegisterTest(AuthBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/form'
        )

    def form_field_test_with_callback(self, callback):
        url = reverse('authentication:register')
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

        form.find_element(By.NAME, 'username').send_keys('Test')
        form.find_element(By.NAME, 'email').send_keys('test@gmail.com')
        form.find_element(By.NAME, 'password').send_keys('Test123')

        callback(form)
        return form

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'username')
            username_field.clear()
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Campo de usuário vazio.', message)
        self.form_field_test_with_callback(callback)

    def test_exist_username_error_message(self):
        def callback(form):
            username = 'UserExist'
            User.objects.create_user(username=username, password='asd')

            username_field = form.find_element(By.NAME, 'username')
            username_field.clear()
            username_field.send_keys(username)
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Nome de usuário indisponível.', message)
        self.form_field_test_with_callback(callback)

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

    def test_exist_email_error_message(self):
        def callback(form):
            email = 'usedemail@gmail.com'
            User.objects.create_user(
                username='User',
                password='Pass',
                email=email
            )

            email_field = form.find_element(By.NAME, 'email')
            email_field.clear()
            email_field.send_keys(email)
            email_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Email indisponível.', message)
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

    def test_register_is_success(self):
        def callback(form):
            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Usuário criado com sucesso.', message)
        self.form_field_test_with_callback(callback)
