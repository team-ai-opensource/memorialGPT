from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Post
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import json
from django.views.decorators.csrf import csrf_exempt


# BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# .env 파일 로드
load_dotenv(os.path.join(BASE_DIR, '.env'))

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=API_KEY)

def home(request):
    return render(request, 'home.html')

def read_post(request):
    posts = Post.objects.order_by('-date').all()
    return render(request, 'post_list.html', {"posts": posts})

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
            post_prompt = post_prompt + f"(id: {post.id}, 제목 : {post.title}, 내용 : {post.content})\n"

        print(post_prompt)

        completion = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"""
            너는 내 기억을 바탕으로 답변을 주는 AI야.
            내가 메모한 기억들을 줄 건데, 그 내용들을 바탕으로 내 질문에 대해 답변해줘.
            답변양식은 json 형식으로 주면 되는데, 그 양식은 맨 하단에 줄거야.
             

            - 만약 그 메모로 이동이 필요하다고 질문에서 언급했으면
            = type : id 이고 출력은 그냥 그 post의 id만 출력해줘
             
            - 그냥 일반적인 메모에 대한 답변인 경우
            = type : common 이고 출력은 그냥 메모를 바탕으로 한 답변을 해 주면 돼.
             
            - 새로운 메모를 작성해달라는 질문이 왔을 경우
            = {{ "type" : "create", "title": "[[추가할 메모의 제목]]", "content": "[[추가할 메모의 내용]]", "answer": "메모를 추가했습니다."}}
            
            메모 :
            {post_prompt}

            위의 메모내용들을 가지고 내 질문에 답변 하면 돼.

            답변 예시 :
            {{ "type" : "id", "answer": 3 }}
            {{ "type" : "id", "answer": 6 }}
            {{ "type" : "id", "answer": 9 }}
            {{ "type" : "common", "answer": "내 구글 아이디는 ~~ 고 내 비번은 ~~ 야" }}
            {{ "type" : "common", "answer": "24년 5월 13일날 한 일에 대한 메모는 존재하지 않습니다." }}
            {{ "type" : "create", "title": "24년 6월 10일 일기", "content": "오늘은 친구와 치킨을 먹었다. 굉장히 맛있었다. ~~", "answer": "메모를 추가했습니다."}}
            {{ "type" : "create", "title": "현호의 모험", "content": "현호는 오늘도 한 숨을 쉬며, 새로운 인생을 시작할 준비를 하고 ... ~~", "answer": "메모를 추가했습니다."}}

            """},
            {"role": "user", "content": my_message}
        ]
        )

        message = completion.choices[0].message.content


        dict_message = json.loads(message)
        print(dict_message)

        if (dict_message['type'] == "create"):
            new_post = Post(title=dict_message['title'], content=dict_message['content'])
            new_post.save()

        return JsonResponse(dict_message)

@csrf_exempt
def delete_post(request, id):
    # print(request)    
    if request.method == 'DELETE':        
        # 특정 ID로 BlogPost 객체 가져오기
        post = get_object_or_404(Post, id=id)
        # 객체 삭제
        post.delete()

        return HttpResponse('성공')




