from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('post_list', views.read_post),
    path('post/<int:id>', views.post_page),
    path('create', views.create_post),
    path('update/<int:id>', views.update_post),
    path('chat', views.post_chat),
    path('delete/<int:id>', views.delete_post),
]
