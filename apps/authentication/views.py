from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from apps.validation import validation


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
            return redirect('/auth/register/')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário criado com sucesso')
            return redirect('/auth/login')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect('/auth/register/')

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
            return redirect('/auth/login')
        
        try:
            username = User.objects.filter(email=email).first()
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('/')
            else:
                messages.error(request, 'Falha no login.')
                return redirect('/auth/login')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect('/auth/login')

def logout(request):
    try:
        auth.logout(request)
        messages.success(request, 'Logout realizado com sucesso.')
        return redirect('/auth/login')
    except:
        messages.error(request, 'Erro interno do sistema ocorreu.')
        return redirect('/auth/login')