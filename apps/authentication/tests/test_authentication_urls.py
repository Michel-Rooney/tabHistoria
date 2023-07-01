from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class AuthenticationURLsTest(TestCase):
    @parameterized.expand([
            ('authentication:register', '/auth/register/'),
            ('authentication:login', '/auth/login/'),
            ('authentication:logout', '/auth/logout/'),
        ])
    def test_authentication_url_is_correct(self, path_name, correct_url):
        url = reverse(path_name)
        self.assertEqual(url, correct_url)
