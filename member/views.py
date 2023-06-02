from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib import messages
from django.core.paginator import Paginator


@login_required(login_url='login')
def profile(request, id):
    if request.method == 'GET':
        member = get_object_or_404(User, id=id)
        posts = Post.objects.filter(creator=member.id).order_by('-creation_date')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        counter = paginator.page_range.start + posts.number - 1
        return render(request, 'pages/profile.html', {'member': member, 'posts': posts, 'counter':counter, 'page_quantity':3})
    
@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        post = Post(title=title, creator=request.user, content=text_content)
        post.save()

        return redirect(f'/member/profile/{request.user.id}')
    
def post_viewer(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    return render(request, 'pages/post_viewer.html', {'post':post, 'comments':comments})

@login_required(login_url='/login')
def vote(request, id):
    vote = request.POST.get('vote')
    type = request.POST.get('type')
    id_post = request.POST.get('id-post')
    
    if type == 'comment':
        entity = get_object_or_404(Comment, id=id)
    else:
        entity = get_object_or_404(Post, id=id)
        
    user_liked = entity.users_liked.filter(id=request.user.id).exists()
    user_disliked = entity.users_disliked.filter(id=request.user.id).exists()
    

    if vote == 'up' and not user_liked:
        entity.users_liked.add(request.user.id)
        entity.users_disliked.remove(request.user.id)
        entity.likes += 1

    if vote == 'down' and not user_disliked:
        entity.users_disliked.add(request.user.id)
        entity.users_liked.remove(request.user.id)
        entity.likes -= 1

    entity.save()
    return redirect(f'/member/post/{id_post}/')
    
@login_required(login_url='/login')
def comment(request, id):
    content = request.POST.get('text-content')
    type = request.POST.get('type')
    id_post = request.POST.get('id-post')

    if type == 'post':
        entity = get_object_or_404(Post, id=id)
    else:
        entity = get_object_or_404(Comment, id=id)

    new_comment = Comment (
        creator = request.user,
        content = content
    )

    new_comment.save()
    entity.comments.add(new_comment.id)
    entity.save()
    return redirect(f'/member/post/{id_post}')

def render_post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'partials/render_post.html', {'post': post})

@login_required(login_url='/login')
def delete_post(request, pk_post, pk_member):
    member = get_object_or_404(User, pk=pk_member)

    if request.user.id != member.id:
        messages.error(request, 'A ação de deletar um post de outro usuário não é permitida para o usuário atual.')
        return redirect(f'/member/profile/{member.id}/')

    post = get_object_or_404(Post, pk=pk_post)
    post.delete()
    messages.success(request, 'Post excluído com sucesso.')
    return redirect(f'/member/profile/{member.id}/')

@login_required(login_url='/login')
def update_post(request, pk_post, pk_member):
    member = get_object_or_404(User, pk=pk_member)
    post = get_object_or_404(Post, pk=pk_post)

    if request.user.id != member.id:
        messages.error(request, 'A ação de atualizar um post de outro usuário não é permitida para o usuário atual.')
        return redirect(f'/member/profile/{member.id}/')
    
    elif request.method == 'GET':
        return render(request, 'pages/update_post.html', {'post': post, 'member': member})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        post.title = title
        post.content = text_content
        post.save()

        return redirect(f'/member/profile/{member.id}')
