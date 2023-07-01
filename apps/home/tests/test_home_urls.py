from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class HomeURLsTest(TestCase):
    @parameterized.expand([
        ('home:home', '/'),
        ('home:about', '/about/')
    ])
    def test_home_url_is_correct(self, path_name, correct_url):
        url = reverse(path_name)
        self.assertEqual(url, correct_url)
