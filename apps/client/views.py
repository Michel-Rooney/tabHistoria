from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.post.models import Post
from django.core.paginator import Paginator
from django.contrib import messages
from apps.validation import validation


def profile(request, id):
    if request.method == 'GET':
        client = get_object_or_404(User, id=id)
        posts = Post.objects.filter(creator=client.id).order_by('-creation_date')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        counter = paginator.page_range.start + posts.number - 1
        return render(request, 'pages/profile.html', {'client': client, 'posts': posts, 'counter':counter, 'page_quantity':3})

@login_required(login_url='auth/login/')
def update_profile(request, id):
    profile = User.objects.filter(id=id).first()
    
    if not profile.id == request.user.id:
        messages.error(request, 'Você não tem permissão de acesso.')
        return redirect(f'/client/profile/{profile.id}/')
    
    if request.method == 'GET':
        return render(request, 'pages/update_profile.html', {'profile': profile})
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if not validation.update_profile_is_valid(request, profile, username, email):
            return redirect(f'/client/update_profile/{profile.id}/')

        profile.username = username
        profile.email = email
        profile.save()

        return redirect(f'/client/update_profile/{profile.id}/')