from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def read_post(request):
    print(request)
    return JsonResponse({"message": "hello"})