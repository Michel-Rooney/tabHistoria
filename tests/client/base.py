import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_edge_browser
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


class ClientBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_edge_browser()
        self.user = self.login_client()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qtd=10):
        time.sleep(qtd)

    def login_client(self):
        email = 'test@gmail.com'
        password = 'Test123'
        user = User.objects.create_user(
            username='UserTest',
            password=password,
            email=email
        )

        url = reverse('authentication:login')
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

        form.find_element(By.NAME, 'email').send_keys(email)
        form.find_element(By.NAME, 'password').send_keys(password)

        form.submit()
        return user
