from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':
        posts = Post.objects.filter(creator=request.user.id)
        print(posts)
        return render(request, 'pages/profile.html', {'posts': posts})
    
@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        post = Post(title=title, creator=request.user, content=text_content)
        post.save()

        return redirect('/member/teste_render/')
    
def teste_render(request):
    post = Post.objects.first()
    return render(request, 'pages/render.html', {'post':post})