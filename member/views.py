from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment


@login_required(login_url='login')
def profile(request, id):
    if request.method == 'GET':
        member = get_object_or_404(User, id=id)
        posts = Post.objects.filter(creator=member.id)

        post = Post.objects.first()
        print(post)
        print(post.comments.first())
        com = Comment.objects.first()
        print(com.comments.exists())

        return render(request, 'pages/profile.html', {'member': member, 'posts': posts})
    
@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text-content')

        post = Post(title=title, creator=request.user, content=text_content)
        post.save()

        return redirect(f'/member/profile')
    
def post_viewer(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    return render(request, 'pages/post_viewer.html', {'post':post, 'comments':comments})

@login_required(login_url='/login')
def vote(request, id):
    vote = request.POST.get('vote')
    post = get_object_or_404(Post, id=id)
    user_liked = post.users_liked.filter(id=request.user.id).exists()
    user_disliked = post.users_disliked.filter(id=request.user.id).exists()
    

    if vote == 'up' and not user_liked:
        post.users_liked.add(request.user.id)
        post.users_disliked.remove(request.user.id)
        post.likes += 1

    if vote == 'down' and not user_disliked:
        post.users_disliked.add(request.user.id)
        post.users_liked.remove(request.user.id)
        post.likes -= 1

    post.save()
    return redirect(f'/member/post/{post.id}/')
    
@login_required(login_url='/login')
def comment_post(request, id):
    content = request.POST.get('text-content')
    post = get_object_or_404(Post, id=id)

    comment = Comment(
        creator=request.user,
        content=content
    )

    comment.save()
    post.comments.add(comment.id)
    post.save()
    return redirect(f'/member/post/{post.id}')

@login_required(login_url='/login')
def comment_comment(request, id):
    content = request.POST.get('text-content')
    comment = get_object_or_404(Comment, id=id)

    new_comment = Comment(
        creator=request.user,
        content=content
    )

    new_comment.save()
    comment.comments.add(new_comment.id)
    comment.save()
    # post = Post.objects.get(comments=comment)
    return redirect(f'/member/post/1')

    