from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from member.models import Post
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.contrib import messages
from validation import validation


def home(request):
    if request.method == 'GET':
        category = request.GET.get('category')

        if category == 'recent':
            posts = Post.objects.all().order_by('-creation_date')
        else:
            posts = Post.objects.annotate(date=TruncDate('creation_date')).order_by('-date', '-likes')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'pages/index.html', {'posts': posts, 'category':category, 'page_quantit': 10})

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, 'Necessário fazer logout para acessar a página.')
            return redirect('/')
        return render(request, 'pages/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validation.register_is_valid(request, username, email, password):
            return redirect('/register/')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário criado com sucesso')
            return redirect('/login/')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect('/register/')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, 'Necessário fazer logout para acessar a página.')
            return redirect('/')
        return render(request, 'pages/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validation.login_is_valid(request, email, password):
            return redirect('/login')
        
        try:
            username = User.objects.filter(email=email).first()
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('/')
            else:
                messages.error(request, 'Falha no login.')
                return redirect('/login')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect('/login')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('/login')
