import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import PostBaseTest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.functional_test
class PostUpdateTest(PostBaseTest):
    def comment_test_with_callback(self, callback, post):
        data = {'id': post.id}
        url = reverse('post:post_viewer', kwargs=data)
        self.browser.get(self.live_server_url + url)

        callback()

    def test_post_comment_is_success(self):
        post = self.create_post()

        def callback():
            self.browser.find_element(
                By.ID, 'respond-post'
            ).click()

            wait = WebDriverWait(self.browser, 1)
            modal = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[1]'))
            )

            self.sleep(0.1)
            modal.send_keys(Keys.TAB * 2 + 'Test Comment Post')
            self.browser.find_element(
                By.XPATH, '/html/body/div[1]/div/div/form/div[2]/button[2]'
            ).click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Comentario feito com sucesso.', message)
        self.comment_test_with_callback(callback, post)

    def test_post_comment_comment_is_success(self):
        post = self.create_post()
        comment = self.create_comment(post)

        def callback():
            self.browser.find_element(
                By.ID, f'respond-comment{comment.id}'
            ).click()

            wait = WebDriverWait(self.browser, 1)
            modal = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/main/section[3]/div/div[2]'))
            )

            modal.send_keys(Keys.TAB * 2 + 'Test Comment Comment')

            path_button_respond = (
                '/html/body/main/section[3]/div/div[2]/'
                'div/div/form/div[2]/button[2]'
            )
            self.browser.find_element(By.XPATH, path_button_respond).click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Comentario feito com sucesso.', message)
        self.comment_test_with_callback(callback, post)

    def test_post_comment_is_not_valid_error_message(self):
        post = self.create_post()

        def callback():
            self.browser.find_element(
                By.ID, 'respond-post'
            ).click()

            wait = WebDriverWait(self.browser, 1)
            modal = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[1]'))
            )

            self.sleep(0.1)
            modal.send_keys(Keys.TAB * 2 + ' ')
            self.browser.find_element(
                By.XPATH, '/html/body/div[1]/div/div/form/div[2]/button[2]'
            ).click()

            message = self.browser.find_element(
                By.CLASS_NAME, 'message-alert'
            ).text

            self.assertIn('Campo de comentário vazio.', message)
        self.comment_test_with_callback(callback, post)
