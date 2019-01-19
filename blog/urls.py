from django.urls import path
from . import views
from users import views as user_views
from .views import *

urlpatterns = [
    path('', views.home_view,name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(),name='user-posts'),
    path('topic/<post_title>', views.getTopic,name='topic-posts'),
    path('post/<pk>/', views.getPost,name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(),name='post-delete'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),

    path('comment/<int:pk>/update', CommentUpdateView.as_view(),name='comment-update'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(),name='comment-delete'),
    path('comment/new', CommentCreateView.as_view(),name='comment-create'),

    path('about/', views.about,name='blog-about'),

]
