import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import PostBaseTest


@pytest.mark.functional_test
class PostUpdateTest(PostBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/form'
        )

    def form_field_test_with_callback(self, callback):
        post = self.create_post()
        data = {
            'pk_post': post.id,
            'pk_client': self.user.id
        }
        url = reverse('post:update_post', kwargs=data)
        self.browser.get(self.live_server_url + url)
        form = self.get_form()

        callback(form)
        return form

    def test_post_update_invalid_request(self):
        data = {
            'pk_post': 999,
            'pk_client': 999
        }

        url = reverse('post:update_post', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(
            By.TAG_NAME, 'body'
        ).text

        self.assertIn('Invalid request', message)

    def test_post_update_is_not_allowed_for_the_current_user(self):
        post = self.create_post()
        incorrect_user = self.create_user()
        data = {
            'pk_post': post.id,
            'pk_client': incorrect_user.id
        }

        url = reverse('post:delete_post', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(
            By.CLASS_NAME, 'message-alert'
        ).text

        correct_message = (
            'A ação de deletar um post de outro usuário '
            'não é permitida para o usuário atual.'
        )
        self.assertIn(correct_message, message)

    def test_empty_title_create_post_error_message(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.clear()
            title_field.send_keys(' ')
            title_field.send_keys(Keys.TAB)

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Preencha todos os campos necessários.', message)
        self.form_field_test_with_callback(callback)

    def test_empty_content_create_post_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'title').send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
            textarea.send_keys(Keys.CONTROL + 'a')
            textarea.send_keys(Keys.BACKSPACE)
            textarea.send_keys(' ')

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Preencha todos os campos necessários.', message)
        self.form_field_test_with_callback(callback)

    def test_create_post_title_max_length_error_message(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.clear()
            title_field.send_keys('A' * 101)

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Título muito longo.', message)
        self.form_field_test_with_callback(callback)

    def test_update_post_is_success(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.send_keys(' Success')
            title_field.send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
            textarea.send_keys(' Success')

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Post atualizado com sucesso.', message)
        self.form_field_test_with_callback(callback)
