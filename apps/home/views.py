from django.shortcuts import render, HttpResponse
from apps.post.models import Post
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator


def home(request):
    if request.method == 'GET':
        category = request.GET.get('category')

        if category == 'recent':
            posts = Post.objects.all().order_by('-creation_date')
        else:
            posts = Post.objects.annotate(
                date=TruncDate('creation_date')).order_by('-date', '-likes')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts': posts, 'category': category, 'page_quantit': 10}
        return render(request, 'pages/index.html', context=context)
    return HttpResponse("Invalid request")


def about(request):
    if request.method == 'GET':
        return render(request, 'pages/about.html')
    return HttpResponse("Invalid request")
