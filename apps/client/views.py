from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.post.models import Post
from django.core.paginator import Paginator


@login_required(login_url='login')
def profile(request, id):
    if request.method == 'GET':
        client = get_object_or_404(User, id=id)
        posts = Post.objects.filter(creator=client.id).order_by('-creation_date')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        counter = paginator.page_range.start + posts.number - 1
        return render(request, 'pages/profile.html', {'client': client, 'posts': posts, 'counter':counter, 'page_quantity':3})
