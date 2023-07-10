import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import PostBaseTest


@pytest.mark.functional_test
class PostCreateTest(PostBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/form'
        )

    def form_field_test_with_callback(self, callback):
        url = reverse('post:post')
        self.browser.get(self.live_server_url + url)
        form = self.get_form()

        callback(form)
        return form

    def test_empty_title_create_post_error_message(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.send_keys(' ')
            title_field.send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
            textarea.send_keys('Test Content')

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Preencha todos os campos necessários.', message)
        self.form_field_test_with_callback(callback)

    def test_empty_content_create_post_error_message(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.send_keys('Test Title')
            title_field.send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
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
            title_field.send_keys('A' * 101)
            title_field.send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
            textarea.send_keys('Test Content')

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Título muito longo.', message)
        self.form_field_test_with_callback(callback)

    def test_create_post_is_success(self):
        def callback(form):
            title_field = form.find_element(By.NAME, 'title')
            title_field.send_keys('Test Title')
            title_field.send_keys(Keys.TAB)

            textarea = self.browser.switch_to.active_element
            textarea.send_keys('Test Content')

            form.submit()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Post criado com sucesso', message)
        self.form_field_test_with_callback(callback)
