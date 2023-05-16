from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':        
        return render(request, 'pages/profile.html')
    
@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        return render(request, 'pages/post.html')
    elif request.method == 'POST':
        text_content = request.POST.get('text-content')
        return render(request, 'pages/render.html')
    
def renderr(request):
    return render(request, 'pages/render.html')