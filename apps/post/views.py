from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.post.models import Post, Comment
from apps.validation import validation
from django.contrib import messages


@login_required(login_url='/auth/login')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        if not validation.post_is_valid(request, title, text_content):
            return redirect(f'/post')

        try:
            post = Post(title=title.strip(), creator=request.user, content=text_content)
            post.save()
            messages.success(request, 'Post criado com sucesso')
            return redirect(f'/client/profile/{request.user.id}')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect(f'/post/{post.id}')

def post_viewer(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    return render(request, 'pages/post_viewer.html', {'post':post, 'comments':comments})

def render_post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'partials/render_post.html', {'post': post})

@login_required(login_url='/auth/login')
def delete_post(request, pk_post, pk_client):
    client = get_object_or_404(User, pk=pk_client)

    if request.user.id != client.id:
        messages.error(request, 'A ação de deletar um post de outro usuário não é permitida para o usuário atual.')
        return redirect(f'/client/profile/{client.id}/')

    try:
        post = get_object_or_404(Post, pk=pk_post)
        post.delete()
        messages.success(request, 'Post excluído com sucesso.')
        return redirect(f'/client/profile/{client.id}/')
    except:
        messages.error(request, 'Erro interno do sistema ocorreu.')
        return redirect(f'/client/profile/{client.id}/')

@login_required(login_url='/auth/login')
def update_post(request, pk_post, pk_client):
    post = get_object_or_404(Post, pk=pk_post)
    client = get_object_or_404(User, pk=pk_client)

    if request.user.id != client.id:
        messages.error(request, 'A ação de atualizar um post de outro usuário não é permitida para o usuário atual.')
        return redirect(f'/client/profile/{client.id}/')
    
    elif request.method == 'GET':
        return render(request, 'pages/update_post.html', {'post': post, 'client': client})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        if not validation.post_is_valid(request, title, text_content):
            return redirect(f'/client/update_post/{post.id}/{client.id}/')

        try:
            post.title = title
            post.content = text_content
            post.save()
            return redirect(f'/client/profile/{client.id}')
        except:
            messages.error(request, 'Erro interno do sistema ocorreu.')
            return redirect(f'/client/profile/{client.id}')

@login_required(login_url='/auth/login')
def vote(request, id):
    vote = request.POST.get('vote')
    type = request.POST.get('type')
    id_post = request.POST.get('id-post')
    
    if type == 'comment':
        entity = get_object_or_404(Comment, id=id)
    else:
        entity = get_object_or_404(Post, id=id)
        
    
    try:
        user_liked = entity.users_liked.filter(id=request.user.id).exists()
        user_disliked = entity.users_disliked.filter(id=request.user.id).exists()
        

        if vote == 'up' and not user_liked:
            entity.users_liked.add(request.user.id)
            entity.users_disliked.remove(request.user.id)   
            entity.likes += 1
            messages.success(request, 'Like realizado com sucesso.')

        if vote == 'down' and not user_disliked:
            entity.users_disliked.add(request.user.id)
            entity.users_liked.remove(request.user.id)
            entity.likes -= 1
            messages.success(request, 'Deslike realizado com sucesso.')

        entity.save()
        return redirect(f'/post/{id_post}/')
    except:
        messages.error(request, 'Erro interno do sistema ocorreu.')
        return redirect(f'/post/{id_post}/')
    
@login_required(login_url='/auth/login')
def comment(request, id):
    content = request.POST.get('text-content')
    type = request.POST.get('type')
    id_post = request.POST.get('id-post')

    if not validation.make_comment_is_valid(request, content):
        return redirect(f'/client/post/{id_post}')

    if type == 'post':
        entity = get_object_or_404(Post, id=id)
    else:
        entity = get_object_or_404(Comment, id=id)

    try:
        new_comment = Comment (
            creator = request.user,
            content = content
        )

        new_comment.save()
        entity.comments.add(new_comment.id)
        entity.save()
        messages.success(request, 'Comentario feito com sucesso.')
        return redirect(f'/post/{id_post}')
    except:
        messages.error(request, 'Erro interno do sistema ocorreu.')
        return redirect(f'/post/{id_post}')