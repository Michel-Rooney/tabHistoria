from django.core.exceptions import ValidationError
from .test_post_base import PostTestBase


class RecipeCategoryModelTest(PostTestBase):
    def setUp(self) -> None:
        self.post = self.make_post()
        return super().setUp()

    def test_post_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.post),
            self.post.title
        )

    def test_recipe_category_model_name_max_length_is_100_chars(self):
        self.post.title = 'A' * 101
        with self.assertRaises(ValidationError):
            self.post.full_clean()
