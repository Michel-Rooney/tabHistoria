import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth.models import User

from .base import ClientBaseTest


@pytest.mark.functional_test
class ClientUpdateProfileTest(ClientBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/form'
        )

    def form_field_test_with_callback(self, callback):
        data = {'id': self.user.id}
        url = reverse('client:update_profile', kwargs=data)
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

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

    def test_update_profile_is_success(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'username')
            email_field = form.find_element(By.NAME, 'email')

            username_field.send_keys('valid')
            email_field.clear()
            email_field.send_keys('success@gmail.com')
            form.submit()
            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Usuário atualizado com sucesso', message)
        self.form_field_test_with_callback(callback)
