from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from apps.validation import validation
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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
            username=username.strip(),
            email=email.strip(),
            password=password)
        user.save()
        messages.success(request, 'Usuário criado com sucesso.')
        return redirect('/auth/login/')
    return HttpResponse("Invalid request")


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            message = 'Necessário fazer logout para acessar a página.'
            messages.error(request, message)
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


@login_required(login_url='/auth/login/', redirect_field_name='next')
def logout(request):
    if not request.POST:
        messages.error(request, 'Requisição de logout inválida.')
        return redirect(reverse('home:home'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'User logout inválido.')
        return redirect(reverse('home:home'))

    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect(reverse('authentication:login'))
