import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse

from .base import PostBaseTest


@pytest.mark.functional_test
class PostUpdateTest(PostBaseTest):
    def arrow_test_with_callback(self, callback, post):
        data = {'id': post.id}
        url = reverse('post:post_viewer', kwargs=data)
        self.browser.get(self.live_server_url + url)

        callback()

    def test_post_like_is_success(self):
        post = self.create_post()

        def callback():
            arrow = self.browser.find_element(
                By.XPATH, '/html/body/main/section[1]/aside/form/button[1]'
            )
            arrow.click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Like realizado com sucesso.', message)
        self.arrow_test_with_callback(callback, post)

    def test_post_deslike_is_success(self):
        post = self.create_post()

        def callback():
            arrow = self.browser.find_element(
                By.XPATH, '/html/body/main/section[1]/aside/form/button[2]'
            )
            arrow.click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Deslike realizado com sucesso.', message)
        self.arrow_test_with_callback(callback, post)

    def test_post_comment_like_is_success(self):
        post = self.create_post()
        self.create_comment(post)

        def callback():
            arrow = self.browser.find_element(
                By.XPATH,
                '/html/body/main/section[3]/aside/form/button[1]'
            )
            arrow.click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Like realizado com sucesso.', message)
        self.arrow_test_with_callback(callback, post)

    def test_post_comment_deslike_is_success(self):
        post = self.create_post()
        self.create_comment(post)

        def callback():
            arrow = self.browser.find_element(
                By.XPATH,
                '/html/body/main/section[3]/aside/form/button[2]'
            )
            arrow.click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Deslike realizado com sucesso.', message)
        self.arrow_test_with_callback(callback, post)
