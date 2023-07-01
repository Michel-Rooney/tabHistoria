from django.core.exceptions import ValidationError
from .test_post_base import PostTestBase
from apps.post.models import Comment


class RecipeCategoryModelTest(PostTestBase):
    def setUp(self) -> None:
        self.comment = self.make_comment()
        return super().setUp()

    def test_post_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.comment),
            self.comment.content[0:50]
        )

    def test_post_comment_model_list_comment_is_correct(self):
        for i in range(1, 5):
            comment = Comment.objects.create(
                creator=self.make_client(
                    username=f'name{i}',
                    email=f'email{i}@gmail.com'
                ),
                content='Content'
            )
            comment.save()
            self.comment.comments.add(comment.id)

        list_comment_size = len(list(self.comment.list_comments()))
        self.assertEqual(list_comment_size, 3)
