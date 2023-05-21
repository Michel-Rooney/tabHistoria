from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from member.models import Post

from django.db.models.functions import TruncDate
from django.core.paginator import Paginator

def home(request):
    if request.method == 'GET':
        category = request.GET.get('category')

        print(request.build_absolute_uri())

        if category == 'recent':
            posts = Post.objects.all().order_by('-creation_date')
        else:
            posts = Post.objects.annotate(date=TruncDate('creation_date')).order_by('date', '-likes')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'pages/index.html', {'posts': posts, 'category':category})

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'pages/register.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        return redirect('/login')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'pages/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = User.objects.filter(email=email).first()
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('/login')


def logout(request):
    auth.logout(request)
    return redirect('/login')




# TODO: Fazer as mensagens de respostas
# TODO: Fazer os regex
# TODO: Fazer os redirecionamentos