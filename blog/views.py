from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from users import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            messages.success(request, f"Your Comment Has Been Posted!")
            pass

    else:
        c_form = NewCommentForm(instance=request.user)

#Search for the cliecked-on post
    if (pk):
        context = {
            'posts': Post.objects.all(),
            'comments': Comment.objects.all(),
            'obj': Post.objects.get(id=pk),
            'comment_form': c_form}


    return render(request, 'blog/post_detail.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

@login_required
def home_view(request):
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
            'pages' : pages}

    return render(request, 'blog/home.html', context)

def getTopic(request, post_title=None):

    if (post_title):
        posts = Post.objects.filter(topics__title=post_title)
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
            'pages': pages}


    return render(request, 'blog/topic_posts.html', context)

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
    fields = ['title', 'image', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content']


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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['image', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['image', 'content']


    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if(self.request.user == comment.author):
            return True
        else:
            return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if(self.request.user == comment.author):
            return True
        else:
            return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
