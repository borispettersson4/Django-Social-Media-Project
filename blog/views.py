from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from users.models import *
from django.views.generic import *
from django.contrib.messages.views import *
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from chartjs import *
from django import template
from django.db.models import Q
from bootstrap_modal_forms.mixins import *
from django import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
import os
import json
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

def home(request):
    context = {
        'posts': Post.objects.all(),
        'comments': Comment.objects.all(),
        'conjunction': {
                        'posts': Post.objects.all(),
                        'comments': Comment.objects.all()
                       }
    }
    return render(request, 'blog/home.html', context)

def getPost(request, pk=None):

#Get the Add Comment Form
    if (request.method == 'POST'):
        c_form = NewCommentForm(request.POST, request.FILES, instance=request.user)
        if (c_form.is_valid()):
            c_form.save()
            cont = c_form.cleaned_data.get('content')
            post = Post.objects.get(id=pk)
            img = c_form.cleaned_data.get('image')
            author = request.user
            comment = Comment(content=cont,post=post,image=img,author=author)
            comment.save()
            new_activity = Activity(post=post, author=author, message="posted a comment")
            new_activity.save()
            pass

    else:
        c_form = NewCommentForm(instance=request.user)

#Search for the cliecked-on post
    if (pk):
        context = {
            'posts': Post.objects.all(),
            'comments': Comment.objects.all(),
            'obj': Post.objects.get(id=pk),
            'comment_form': c_form,
            'likes' : Like.objects.all(),
            'user' : request.user,
            'activities' : Activity.objects.filter(post=Post.objects.get(id=pk))}


    return render(request, 'blog/post_detail.html', context)

def openPost(request, pk=None):
    post_num = 0
    if request.method == 'POST':
            post_num = pk


    posts = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context = {
            'posts': posts,
            'profile': request.user.profile,
            'page_obj': paginator,
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'user' : request.user,
            'obj_posts': Post.objects.all(),
            'obj': Post.objects.get(id=pk),
            'activities' : Activity.objects.filter(post=Post.objects.get(id=pk))
              }

    return render('blog/.html')

class PostView(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'blog/post_modal.html'
    form_class = ViewPostForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

class PostModalView(DetailView):
    model = Post

@login_required
def home_view(request, pk=1):

    if (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES, instance=request.user)
        if(post_form.is_valid()):
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user)
            new_post.save()
    else:
        post_form = NewPostForm(instance=request.user)


    posts = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context = {
            'posts': posts,
            'profile': request.user.profile,
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'activities' : Activity.objects.all(),
            'user' : request.user,
            'obj' : Post.objects.get(id=pk),
            'post_form' : post_form}

#When user clicks on a post
    if request.is_ajax():
        post_id = request.POST.get('id')
        obj = Post.objects.get(id=post_id)

        sub_context = {
            'posts': posts,
            'profile': request.user.profile,
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'replies' : Post.objects.filter(reply=obj),
            'replies-reply' : Post.objects.filter(reply=obj),
            'likes' : Like.objects.all(),
            'user' : request.user,
            'obj' : obj,
            'activities' : Activity.objects.filter(post=Post.objects.get(id=post_id)),
            'post_form' : NewPostForm(instance=request.user)}

        if (request.POST.get('action') == "Comment"):
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=post, author=author, message="posted a comment")
            new_activity.save()
            html = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            html3 = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2, 'post' : html3})


        elif (request.POST.get('action') == "View_Post"):
            html = render_to_string('blog/post.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Post"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                else:
                    likes.delete()
            except:
                pass

            html = render_to_string('blog/post.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Post_Reply"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                else:
                    likes.delete()
            except:
                pass
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/replies.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Feed"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                else:
                    likes.delete()
            except:
                pass

            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "New_Post"):
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})


    return render(request, 'blog/home.html', context)

def get_post(request):
    return HttpResponse('blog/post.html')

def getTopic(request, post_title=None):

    if (post_title):
        posts = Post.objects.filter(topics__title=post_title)
        pages = paginate(request,posts)
        context = {
            'posts': posts,
            'pages': pages['pages']}


    return render(request, 'blog/topic_posts.html', context)

def get_user_information(request, username=None):

    posts = Post.objects.filter(Q(author__username=username) | Q(people__username=username)).order_by('-date_posted').distinct()
    profile = Profile.objects.get(user__username=username)

    #followers_count
    #following_count
    pages = paginate(request,posts)
    context = {
        'posts': posts.distinct(),
        'pages': pages['pages'],
        'followers_count' : profile.followers.count(),
        'following_count' : profile.following.count(),
        'friends_count' : profile.friends.count(),
        'page_obj':pages['page_obj'],
        'profile': profile,
        'comments' : Comment.objects.all(),
        'likes' : Like.objects.all(),
        'user' : request.user,
        'activities' : Activity.objects.filter(author__username=username),
        'images' : Post.objects.filter(Q(author__username=username) & ~Q(image="default.jpg")).order_by('-date_posted'),
        'user_posts' : Post.objects.filter(author__username=username).count(),
        'user_comments' : Comment.objects.filter(author__username=username).count(),
        'obj' : Post.objects.get(id=1),
        'user_likes' : Like.objects.filter(post__author__username=username).count()}

    if request.is_ajax():
        post_id = request.POST.get('id')
        obj = Post.objects.get(id=post_id)

        sub_context = {
            'posts': posts,
            'profile': request.user.profile,
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'replies' : Post.objects.filter(Q(reply=obj)),
            'likes' : Like.objects.all(),
            'user' : request.user,
            'obj' : obj,
            'activities' : Activity.objects.filter(post=Post.objects.get(id=post_id))}

        if (request.POST.get('action') == "Comment"):
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=post, author=author, message="posted a comment")
            new_activity.save()
            html = render_to_string('blog/replies.html', sub_context, request=request)
            return JsonResponse({'form':html})

        if (request.POST.get('action') == "View_Post"):
            html = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html})

    return render(request, 'blog/user_posts.html', context)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class TopicPostListView(ListView):
    model = Post
    template_name = 'blog/topic_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'content', 'topics','people']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content', 'topics']


    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if(self.request.user == post.author):
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if(self.request.user == post.author):
            return True
        else:
            return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

#Extra views

def paginate(request, posts):
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    dict = {'pages':pages,'page_obj':paginator}
    return dict

from django.shortcuts import render_to_response
import random
import datetime
import time

def demo_piechart(request):
    """
    pieChart page
    """
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
    }
    return render(request,'blog/test.html', data)

def validate_username(request):
    post_no = request.GET.get('num', None)
    data = None
    return JsonResponse(data)

class SignUpView(DetailView):
    template_name = 'blog/test.html'
    form_class = UserCreationForm
