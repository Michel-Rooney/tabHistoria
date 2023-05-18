from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from member.models import Post



def home(request):
    posts = Post.objects.all()
    return render(request, 'pages/index.html', {'posts': posts})

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
    return redirect('/')




# TODO: Fazer as mensagens de respostas
# TODO: Fazer os regex
# TODO: Fazer os redirecionamentos