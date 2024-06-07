from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Post
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import json

# BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# .env 파일 로드
load_dotenv(os.path.join(BASE_DIR, '.env'))

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=API_KEY)


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


        Post.objects.filter(id=id).update(title=title, content=content)

        return HttpResponse('성공')
    
def post_chat(request):
    if request.method == 'POST':
        my_message = request.POST["message"]
        # my_message = "구글 아이디 비번 좀 알려줘"

        posts = Post.objects.order_by('-date').all()

        post_prompt = ""
        for post in posts:
            post_prompt = post_prompt + f"(제목 : {post.title} 내용 : {post.content})\n"

        print(post_prompt)

        completion = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        # response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"""
            너는 내 기억을 바탕으로 답변을 주는 AI야.
            내가 메모한 기억들을 줄 건데, 그 내용들을 바탕으로 내 질문에 대해 답변해줘.
             
            메모 :
            {post_prompt}

            위의 메모내용들을 가지고 내 질문에 답변 하면 돼.
            """},
            {"role": "user", "content": my_message}
        ]
        )

        message = completion.choices[0].message.content
        print(message)

        return HttpResponse(message)

    
            




