from django.urls import path
from . import views
from users import views as user_views
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('', views.home_view,name='blog-home'),
    url(r'^ajaxtest/', views.get_post, name='ajaxtest'),
    path('<pk>', views.home_view,name='post-open'),
    path('mobile/notifications', views.notifications,name='notifications'),
    path('mobile/messages', views.messages,name='messages'),
    path('user/<str:username>', views.get_user_information,name='user-posts'),
    path('user/<str:username>/<str:view>', views.get_user_information,name='user-posts'),
    path('group/<str:name>', views.get_group_information,name='group-posts'),
    path('group/<str:name>/<str:view>', views.get_group_information,name='group-posts'),
    path('topic/<topic>', views.getTopic,name='topic-posts'),
    path('post/item/<pk>/', views.getPost,name='post-detail'),
    path('search/<str:query_result>', views.search,name='search'),
    path('post/<int:pk>/update', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(),name='post-delete'),
    path('post/test', PostUpdateView.as_view(),name='post-open2'),
    path('post/new', PostCreateView.as_view(),name='post-create'),
    path('test/', views.test,name='test'),
    path('about/', views.about,name='blog-about'),

]
