from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from apps.validation import validation
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(
                request, 'Necessário fazer logout para acessar a página.')
            return redirect('/')
        return render(request, 'pages/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validation.register_is_valid(request, username, email, password):  # noqa: E501
            return redirect('/auth/register/')
    
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password)
        user.save()
        messages.success(request, 'Usuário criado com sucesso')
        return redirect('/auth/login/')
    return HttpResponse("Invalid request")


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
            return redirect('/auth/login/')
        
        username = User.objects.filter(email=email).first()
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login realizado com sucesso.')
            return redirect('/')
        else:
            messages.error(request, 'Falha no login.')
            return redirect('/auth/login/')
    return HttpResponse("Invalid request")


@login_required(login_url='/auth/login/')
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        messages.success(request, 'Logout realizado com sucesso.')
        return redirect('/auth/login/')
    return HttpResponse("Invalid request")
