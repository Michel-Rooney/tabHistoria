from django.contrib.auth.models import User
from django.contrib import messages
import re


def username_is_valid(request: any, username: str, validation_exist: bool = False) -> bool:
    if len(username.strip()) == 0:
        messages.error(request, 'Campo de usuário vazio.')
        return False

    if validation_exist:
        username_exist = User.objects.filter(username=username).exists()
        if username_exist:
            messages.error(request, 'Nome de usuário indisponível.')
            return False
    
    return True

def email_is_valid(request: any, email: str, validation_exist: bool = False) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # exemplo@email.com

    if len(email.strip()) == 0:
        messages.error(request, 'Campo de email vazio.')
        return False

    if validation_exist:
        email_exist = User.objects.filter(email=email).exists()
        if email_exist:
            messages.error(request, 'Email indisponível.')
            return False
    
    if not re.match(pattern, email):
        messages.error(request, 'Email inválido.')
        return False
    
    return True

def password_is_valid(request: any, password: str) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$'  # Senha123
    
    if len(password.strip()) == 0:
        messages.error(request, 'Campo de senha vazio.')
        return False

    if not re.match(pattern, password):
        messages.error(request, 'Senha inválida')
        return False
    
    return True


def register_is_valid(request: any, username: str, email: str, password: str) -> bool:
    if not username_is_valid(request, username):
        return False
    
    if not email_is_valid(request, email, validation_exist=True):
        return False
    
    if not password_is_valid(request, password):
        return False
    
    return True

def login_is_valid(request: any, email: str, password: str) -> bool:
    if not email_is_valid(request, email):
        return False

    if not password_is_valid(request, password):
        return False

    return True

def post_is_valid(request: any, title: str, content: str) -> bool:
    if len(title.strip()) == 0 or len(content.strip()) == 0:
        messages.error(request, 'Preencha todos os campos necessários.')
        return False
    
    if len(title.strip()) > 100:
        messages.error(request, 'Título muito longo.')

    return True

def make_comment_is_valid(request: any, content: str) -> bool:
    if len(content.strip()) == 0:
        messages.error(request, 'Campo de comentário vazio.')
        return False
    
    return True

def update_profile_is_valid(request: any, profile: object, username: str, email: str) -> str:
    username_validation_exist = False if profile.username == username else True
    email_validation_exist = False if profile.email == email else True
    if not username_is_valid(request, username, validation_exist=username_validation_exist): return False
    if not email_is_valid(request, email, validation_exist=email_validation_exist): return False
    return True