from django.test import TestCase
from django.urls import resolve, reverse
from .. import views
from parameterized import parameterized
from apps.post.models import Post, User


class HomeViewsTest(TestCase):
    @parameterized.expand([
        ('home:home', views.home),
        ('home:about', views.about)
    ])
    def test_home_view_function_is_correct(self, path_name, correct_view):
        view = resolve(reverse(path_name))
        self.assertIs(view.func, correct_view)

    @parameterized.expand([
            ('home:home'),
            ('home:about')
        ])
    def test_home_view_returns_status_code_code_200_OK(self, path_name):
        response = self.client.get(reverse(path_name))
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('home:home', 'pages/index.html'),
        ('home:about', 'pages/about.html')
    ])
    def test_home_view_loads_correct_template(
        self, path_name, correct_template
    ):
        response = self.client.get(reverse(path_name))
        self.assertTemplateUsed(response, correct_template)

    @parameterized.expand([
        ('home:home'),
        ('home:about')
    ])
    def test_home_invalid_request(self, path_name):
        url = reverse(path_name)
        response = self.client.put(url)
        message = response.content.decode('utf-8')
        self.assertEqual(message, "Invalid request")

    def test_home_category_valid(self):
        user = User.objects.create_user(
            username='Category valid', password='123')
        for i in range(0, 3):
            Post.objects.create(
                title=f'Title {i}',
                creator=user,
                content=f'Content {i}'
            )
        url = reverse('home:home')
        response = self.client.get(url, data={'category': 'recent'})
        posts_correct = list(Post.objects.all().order_by('-creation_date'))
        posts = list(response.context['posts'])
        self.assertEqual(posts_correct, posts)
