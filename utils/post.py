from apps.post.models import Comment, Post


def get_comment(**kwargs):
    return Comment.objects.filter(
        **kwargs
    ).select_related(
        'creator'
    ).prefetch_related(
        'comments', 'users_liked', 'users_disliked'
    ).first()


def get_comments(**kwargs):
    return Comment.objects.filter(
        **kwargs
    ).select_related(
        'creator'
    ).prefetch_related(
        'comments', 'users_liked', 'users_disliked'
    )


def get_post(**kwargs):
    return Post.objects.filter(
        **kwargs
    ).select_related(
        'creator'
    ).prefetch_related(
        'users_liked', 'users_disliked', 'comments'
    ).first()


def get_posts(**kwargs):
    return Post.objects.filter(
        **kwargs
    ).select_related(
        'creator'
    ).prefetch_related(
        'users_liked', 'users_disliked', 'comments'
    ).order_by('-creation_date')
