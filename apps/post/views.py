from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.post.models import Post, Comment
from apps.validation import validation
from django.contrib import messages
from django.urls import reverse
from utils.post import get_post


@login_required(login_url='/auth/login/', redirect_field_name='next')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        if not validation.post_is_valid(request, title, text_content):
            return redirect('/post/')

        post = Post(
            title=title.strip(),
            creator=request.user,
            content=text_content
        )
        post.save()
        messages.success(request, 'Post criado com sucesso')
        return redirect(f'/client/profile/{request.user.id}/')
    return HttpResponse("Invalid request")


def post_viewer(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)
        comments = post.comments.all()
        render_post_url = reverse('post:render_post', kwargs={'id': post.id})
        context = {
            'post': post,
            'comments': comments,
            'render_post_url': render_post_url,
        }
        return render(request, 'pages/post_viewer.html', context=context)
    return HttpResponse("Invalid request")


def render_post(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)
        return render(request, 'partials/render_post.html', {'post': post})
    return HttpResponse("Invalid request")


@login_required(login_url='/auth/login/', redirect_field_name='next')
def delete_post(request, pk_post, pk_client):
    if request.method == 'GET':
        client = get_object_or_404(User, pk=pk_client)

        if request.user.id != client.id:
            message = (
                'A ação de deletar um post de outro usuário '
                'não é permitida para o usuário atual.'
            )
            messages.error(request, message)
            return redirect(f'/client/profile/{client.id}/')

        post = get_object_or_404(Post, pk=pk_post)
        post.delete()
        messages.success(request, 'Post excluído com sucesso.')
        return redirect(f'/client/profile/{client.id}/')
    return HttpResponse("Invalid request")


@login_required(login_url='/auth/login/', redirect_field_name='next')
def update_post(request, pk_post, pk_client):
    post = get_post(pk=pk_post)
    client = User.objects.filter(pk=pk_client).first()

    if not post or not client:
        return HttpResponse("Invalid request")

    if request.user.id != client.id:
        message = (
            'A ação de atualizar um post de outro usuário '
            'não é permitida para o usuário atual.'
        )
        messages.error(request, message)
        return redirect(f'/client/profile/{client.id}/')

    elif request.method == 'GET':
        context = {'post': post, 'client': client}
        return render(request, 'pages/update_post.html', context=context)

    else:
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        if not validation.post_is_valid(request, title, text_content):
            data = {'pk_post': post.id, 'pk_client': client.id}
            return redirect(reverse('post:update_post', kwargs=data))

        post.title = title
        post.content = text_content
        post.save()
        messages.success(request, 'Post atualizado com sucesso.')
        return redirect(f'/client/profile/{client.id}/')


@login_required(login_url='/auth/login/', redirect_field_name='next')
def vote(request, id):
    if request.method == 'POST':
        vote = request.POST.get('vote')
        type = request.POST.get('type')
        id_post = request.POST.get('id-post')

        if type == 'comment':
            entity = get_object_or_404(Comment, id=id)
        else:
            entity = get_object_or_404(Post, id=id)

        user_liked = entity.users_liked.filter(
            id=request.user.id).exists()
        user_disliked = entity.users_disliked.filter(
            id=request.user.id).exists()

        if vote == 'up' and not user_liked:
            entity.users_liked.add(request.user.id)
            entity.users_disliked.remove(request.user.id)
            entity.likes += 1
            messages.success(request, 'Like realizado com sucesso.')

        if vote == 'down' and not user_disliked:
            entity.users_disliked.add(request.user.id)
            entity.users_liked.remove(request.user.id)
            messages.success(request, 'Deslike realizado com sucesso.')

        entity.save()
        return redirect(f'/post/{id_post}/')
    return HttpResponse("Invalid request")


@login_required(login_url='/auth/login/', redirect_field_name='next')
def comment(request, id):
    if request.method == 'POST':
        content = request.POST.get('text-content')
        type = request.POST.get('type')
        id_post = request.POST.get('id-post')

        if not validation.make_comment_is_valid(request, content):
            return redirect(f'/post/{id_post}/')

        if type == 'post':
            entity = get_object_or_404(Post, id=id)
        else:
            entity = get_object_or_404(Comment, id=id)

        new_comment = Comment(
            creator=request.user,
            content=content
        )

        new_comment.save()
        entity.comments.add(new_comment.id)
        entity.save()
        messages.success(request, 'Comentario feito com sucesso.')
        return redirect(f'/post/{id_post}/')
    return HttpResponse("Invalid request", status=302)
