import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse

from .base import PostBaseTest


@pytest.mark.functional_test
class PostDeleteTest(PostBaseTest):
    def test_post_delete_is_not_allowed_for_the_current_user(self):
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

    def test_post_delete_client_not_found_error_404(self):
        post = self.create_post()
        data = {
            'pk_post': post.id,
            'pk_client': self.user.id + 1
        }
        url = reverse('post:delete_post', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(
            By.TAG_NAME, 'body'
        ).text

        self.assertIn('Not Found', message)

    def test_post_delete_is_success(self):
        post = self.create_post()
        data = {
            'pk_post': post.id,
            'pk_client': self.user.id
        }
        url = reverse('post:delete_post', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(
            By.CLASS_NAME, 'message-alert'
        ).text

        self.assertIn('Post excluído com sucesso.', message)
