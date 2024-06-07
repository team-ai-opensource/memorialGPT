from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Post
from .forms import PostForm


def read_post(request):
    posts = Post.objects.order_by('-date').all()
    return render(request, 'home.html', {"posts": posts})

def post_page(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'detail.html',{"post": post})

def create_post(request):
    # print(request.POST['title'])
    if request.method == 'POST':
        new_post = Post(title=request.POST['title'], content=request.POST['content'])
        new_post.save()
        
        return HttpResponse('성공')

def update_post(request, id):
    if request.method == 'POST':
        # POST 요청에서 보낸 데이터로 객체의 속성 업데이트
        title = request.POST.get('title')
        content = request.POST.get('content')

        print(content)

        Post.objects.filter(id=id).update(title=title, content=content)

        return HttpResponse('성공')

