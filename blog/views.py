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
from django.utils.datastructures import *
from itertools import chain
import datetime
from django.db.models import Count
from functools import reduce
import operator
from django.urls import resolve
from django.utils import timezone

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
    page_limit = 10;
    today = datetime.datetime.now()
    from django.db.models import Count
    #Get all tags
    tops = Topic.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')
    peps = User.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')

    acts = Activity.objects.filter(post=Post.objects.get(id=pk)).order_by('-date')

    post_id = pk
    obj = Post.objects.get(id=post_id)
    post_form = NewPostForm()

    context = {
            'profile': request.user.profile,
            'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
            'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
            'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
            Notification.objects.filter(recepient=request.user, confirmed=False).count(),
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'activities' : acts,
            'user' : request.user,
            'obj' : Post.objects.get(id=pk),
            'post_form' : post_form,
            'people' : peps,
            'topics' : tops,
            'date' : today,
            'page_limit' : page_limit,
            'replies' : Post.objects.filter(reply=obj).order_by('-date_posted'),
            'replies-reply' : Post.objects.filter(reply=obj).order_by('-date_posted'),
            }

#When user clicks on a post
    if request.is_ajax():
        if(request.POST.get('id')):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
        else:
            post_id = 10
            obj = Post.objects.get(id=post_id)

        sub_context = {
            'profile': request.user.profile,
            'comments' : Comment.objects.all(),
            'replies' : Post.objects.filter(reply=obj).order_by('-date_posted'),
            'replies-reply' : Post.objects.filter(reply=obj).order_by('-date_posted'),
            'likes' : Like.objects.all(),
            'user' : request.user,
            'obj' : obj,
            'activities' : Activity.objects.filter(post=Post.objects.get(id=post_id)),
            'post_form' : post_form,
            'page_limit' : page_limit,
            'slice_custom' : page_limit,
            }

        if (request.POST.get('action') == "Comment"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=obj, author=request.user, type=1)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_activity = Activity(post=post, author=request.user, type=2)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=post, type=1)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            html3 = render_to_string('blog/post_like_comment.html', sub_context, request=request)
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
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            html = render_to_string('blog/post_detail.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Like_Post_Reply"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/replies.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})


        elif (request.POST.get('action') == "New_Post"):
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Delete_Post"):

            post = Post.objects.get(id=post_id)
            post.delete()
            html3 = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            html = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2,'post':html3})

        elif (request.POST.get('action') == "Repost"):

            post = Post.objects.get(id=post_id)
            repost = Post(author=request.user, reply=None, repost=post)
            repost.save()
            new_notification = Notification(sender=request.user, recepient=obj.author, post=repost, type=3)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        #User Actions

        elif (request.POST.get('action') == "Open_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user)
            notifications.delete()
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Open_Requests"):
            requests = Request.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Requests"):
            requets = Request.objects.filter(recepient=request.user)
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Decline_Request"):
            requets = Request.objects.get(id=request.POST.get('request_id'))
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

    #Site Behaviour
        elif (request.POST.get('action') == "Load_Next"):
                page_count = request.POST.get('page_count')
                new_context = sub_context
                new_context["page_limit"] += int(page_count)
                html = render_to_string('blog/replies.html',new_context, request=request)
                return JsonResponse({'form':html})

    elif (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES)
        if(post_form.is_valid()):
            tagfield = post_form.cleaned_data.get('tags')
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user, reply=None)

            #Media filtering
            try:
                media = request.FILES['media']
                url = media.name.lower()
                if (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png')):
                    new_post.image = media
                elif (url.endswith('.mp4') or url.endswith('.ogg') or url.endswith('.webm')):
                    new_post.video = media
            except:
                pass

            new_post.save()
            post_form = NewPostForm()

            if(tagfield):
                #Tag filtering
                try:
                    tag_dict = tagfield.split()
                    for tag in tag_dict:
                        if(tag.startswith("#")):
                            try:
                                try:
                                    topic = Topic.objects.get(title=tag[1:])
                                    new_post.topics.add(topic)
                                except:
                                    topic = Topic(title=tag[1:])
                                    topic.save()
                                    new_post.topics.add(topic)
                            except Exception as e:
                                new_post.content = e

                        elif(tag.startswith("@")):
                            try:
                                try:
                                    person = User.objects.get(username=tag[1:])
                                    new_post.people.add(person)
                                    new_notification = Notification(sender=request.user, recepient=person, post=new_post, type=2)
                                    if(new_notification.sender != new_notification.recepient):
                                        new_notification.save()
                                except Exception as e:
                                    print(f"____________________________{e}")
                            except Exception as e:
                                print(f"____________________________{e}")

                except:
                    pass


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
def home_view(request, pk=3):
    page_limit = 10
    post_form = NewPostForm()
    posts = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, page_limit)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    today = datetime.datetime.now()
    from django.db.models import Count
    #Get all tags
    tops = Topic.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')
    peps = User.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')

    acts = Activity.objects.filter(post__date_posted__day=today.day).order_by('-date')

    context = {
            'posts': posts,
            'profile': request.user.profile,
            'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
            'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
            'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
            Notification.objects.filter(recepient=request.user, confirmed=False).count(),
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'activities' : acts,
            'user' : request.user,
            'obj' : Post.objects.get(id=3),
            'post_form' : post_form,
            'people' : peps,
            'topics' : tops,
            'date' : today,
            'page_limit' : page_limit,
            'search' : request.GET.get('search')
            }

#When user clicks on a post
    if request.is_ajax():
        if(request.POST.get('id')):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
        else:
            post_id = 10
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
            'post_form' : post_form,
            'page_limit' : page_limit,
            'slice_custom' : page_limit,
            }

        if (request.POST.get('action') == "Comment"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=obj, author=request.user, type=1)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_activity = Activity(post=post, author=request.user, type=2)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=post, type=1)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            html3 = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2, 'post' : html3})

        elif (request.POST.get('action') == "View_Post"):
            html = render_to_string('blog/post.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "View_Content"):
            html = render_to_string('blog/content_view.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Like_Post"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Post_Reply"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Feed"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
            except:
                pass

            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/feed.html', sub_context, request=request)
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2})

        elif (request.POST.get('action') == "New_Post"):
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Delete_Post"):

            post = Post.objects.get(id=post_id)
            post.delete()
            html3 = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            html = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2,'post':html3})

        elif (request.POST.get('action') == "Repost"):

            post = Post.objects.get(id=post_id)
            repost = Post(author=request.user, reply=None, repost=post)
            repost.save()
            new_activity = Activity(post=Post.objects.get(id=post_id), author=request.user, type=3)
            new_activity.save()
            #Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=repost, type=3)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        #User Actions

        elif (request.POST.get('action') == "Open_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user)
            notifications.delete()
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Open_Requests"):
            requests = Request.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Requests"):
            requets = Request.objects.filter(recepient=request.user)
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Decline_Request"):
            requets = Request.objects.get(id=request.POST.get('request_id'))
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

    #Site Behaviour
        elif (request.POST.get('action') == "Load_Next"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/feed.html',new_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Load_Next_Reply"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/replies.html',new_context, request=request)
            return JsonResponse({'form':html})

    elif (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES)
        if(post_form.is_valid()):
            tagfield = post_form.cleaned_data.get('tags')
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user, reply=None)

            #Media filtering
            try:
                media = request.FILES['media']
                url = media.name.lower()
                if (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png')):
                    new_post.image = media
                elif (url.endswith('.mp4') or url.endswith('.ogg') or url.endswith('.webm')):
                    new_post.video = media
            except:
                pass

            new_post.save()
            post_form = NewPostForm()

            new_activity = Activity(post=new_post, author=request.user, type=2)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)

            if(tagfield):
                #Tag filtering
                try:
                    tag_dict = tagfield.split()
                    for tag in tag_dict:
                        if(tag.startswith("#")):
                            try:
                                try:
                                    topic = Topic.objects.get(title=tag[1:])
                                    new_post.topics.add(topic)
                                except:
                                    topic = Topic(title=tag[1:])
                                    topic.save()
                                    new_post.topics.add(topic)
                            except Exception as e:
                                new_post.content = e

                        elif(tag.startswith("@")):
                            try:
                                try:
                                    person = User.objects.get(username=tag[1:])
                                    new_post.people.add(person)
                                    new_notification = Notification(sender=request.user, recepient=person, post=new_post, type=2)
                                    if(new_notification.sender != new_notification.recepient):
                                        new_notification.save()
                                except Exception as e:
                                    print(f"____________________________{e}")
                            except Exception as e:
                                print(f"____________________________{e}")

                except:
                    pass

    return render(request, 'blog/home.html', context)

def get_post(request):
    return HttpResponse('blog/post.html')

def search(request, search=None):

    query = request.GET.get('search')

    if(query == None):
        query = request.POST.get('query')

    content_search = []
    topics_search = []
    people_search = []

    content_posts = None
    topics_posts = None
    people_posts = None
    people_circles = None

    #Media filtering
    if(query):
        tag_dict = query.split()
        for tag in tag_dict:
            if(tag.startswith("#")):
                topics_search.append(tag[1:])
            elif(tag.startswith("@")):
                people_search.append(tag[1:])
            else:
                content_search.append(tag)

        if(content_search):
            content_posts = Post.objects.filter(Q(reduce(operator.or_, (Q(content__contains=x) for x in content_search)))).order_by('-date_posted')
            people_posts = Post.objects.filter(Q(reduce(operator.or_, (Q(author__profile__nick__contains=x) for x in content_search))) |
                                               Q(reduce(operator.or_, (Q(author__username__contains=x) for x in content_search)))
                                               ).order_by('-date_posted')
            people_circles = Profile.objects.filter(Q(reduce(operator.or_, (Q(nick__contains=x) for x in content_search))) |
                                               Q(reduce(operator.or_, (Q(user__username__contains=x) for x in content_search)))
                                               ).order_by('-date_active')

        if(topics_search):
            topics_posts = Post.objects.filter(Q(reduce(operator.or_, (Q(topics__title__contains=x) for x in topics_search)))).order_by('-date_posted')
            people_circles = Profile.objects.filter(Q(reduce(operator.or_, (Q(user__post__topics__title=x) for x in topics_search)))).order_by('-date_active')

        if(people_search):
            people_posts = Post.objects.filter(Q(reduce(operator.or_, (Q(author__username__contains=x) for x in people_search)))).order_by('-date_posted')
            people_circles = Profile.objects.filter(Q(reduce(operator.or_, (Q(user__username__contains=x) for x in people_search)))).order_by('-date_active')

    if(content_posts or topics_posts or people_posts):
        posts = people_posts or topics_posts or content_posts
        posts = posts.distinct()
        circles = people_circles
        circles = circles.distinct()
    else:
        posts = Post.objects.none()
        circles = Post.objects.none()

    print(f"TOPICS SEARCH {topics_search}")
    print(f"PERSON SEARCH {people_search}")
    print(f"CONTENT SEARCH {content_search}")
    print(f"QUERY {query}")

    page_limit = 10
    post_form = NewPostForm()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, page_limit)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    today = datetime.datetime.now()
    topic = None
    #Get all tags
    tops = Topic.objects.filter(post__topics__title=topic).annotate(count=Count('post__like')).order_by('-count')
    peps = User.objects.filter(post__topics__title=topic).annotate(count=Count('post__like')).order_by('-count')

    acts = Activity.objects.filter(post__date_posted__day=today.day, post__topics__title=topic).order_by('-date')
    last_acts = Activity.objects.filter(post__topics__title=topic).last()

    context = {
            'posts': posts,
            'profile': request.user.profile,
            'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
            'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
            'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
             Notification.objects.filter(recepient=request.user, confirmed=False).count(),
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'activities' : acts,
            'activities_last' : last_acts,
            'user' : request.user,
            'obj' : Post.objects.get(id=10),
            'post_form' : post_form,
            'people' : peps,
            'topics' : tops,
            'date' : today,
            'page_limit' : page_limit,
            'topic' : topic,
            'search_count' : posts.count(),
            'search_users' : circles.count(),
            'topic_first_post' : Post.objects.filter(topics__title=topic).order_by('date_posted').first(),
            'topic_best_post' : Post.objects.filter(topics__title=topic).annotate(count=Count('like')).order_by('-count').first(),
            'query' : query,
            'circles' : circles,
            'term' : query
            }

#When user clicks on a post
    if request.is_ajax():
        if(request.POST.get('id')):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
        else:
            post_id = 10
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
            'activities_last' : last_acts,
            'post_form' : post_form,
            'page_limit' : page_limit,
            'slice_custom' : page_limit,
            'topic' : topic,
            'topic_first_post' : Post.objects.filter(topics__title=topic).order_by('date_posted').first(),
            'topic_best_post' : Post.objects.filter(topics__title=topic).order_by('like').first(),
            'query' : request.POST.get('query'),
            'circles' : circles,
            'term' : query
            }

        if (request.POST.get('action') == "Comment"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=obj, author=request.user, type=1)
            new_activity.save()
            #Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_activity = Activity(post=post, author=request.user, type=2)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=post, type=1)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            html3 = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2, 'post' : html3})

        elif (request.POST.get('action') == "View_Post"):
            html = render_to_string('blog/post.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "View_Content"):
            html = render_to_string('blog/content_view.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Like_Post"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Post_Reply"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Feed"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
            except:
                pass

            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/feed.html', sub_context, request=request)
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2})

        elif (request.POST.get('action') == "New_Post"):
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Delete_Post"):

            post = Post.objects.get(id=post_id)
            post.delete()
            html3 = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            html = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2,'post':html3})

        elif (request.POST.get('action') == "Repost"):

            post = Post.objects.get(id=post_id)
            repost = Post(author=request.user, reply=None, repost=post)
            repost.save()
            new_activity = Activity(post=Post.objects.get(id=post_id), author=request.user, type=3)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=repost, type=3)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        #User Actions

        elif (request.POST.get('action') == "Open_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user)
            notifications.delete()
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Open_Requests"):
            requests = Request.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Requests"):
            requets = Request.objects.filter(recepient=request.user)
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Decline_Request"):
            requets = Request.objects.get(id=request.POST.get('request_id'))
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})
    #Site Behaviour
        elif (request.POST.get('action') == "Load_Next"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/feed.html',new_context, request=request)
            html2 = render_to_string('blog/feed_circles.html',new_context, request=request)
            return JsonResponse({'form':html, 'main':html2})

        elif (request.POST.get('action') == "Load_Next_Reply"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/replies.html',new_context, request=request)
            return JsonResponse({'form':html})

    elif (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES)
        if(post_form.is_valid()):
            tagfield = post_form.cleaned_data.get('tags')
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user, reply=None)

            #Media filtering
            try:
                media = request.FILES['media']
                url = media.name.lower()
                if (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png')):
                    new_post.image = media
                elif (url.endswith('.mp4') or url.endswith('.ogg') or url.endswith('.webm')):
                    new_post.video = media
            except:
                pass

            new_post.save()
            post_form = NewPostForm()

            new_activity = Activity(post=new_post, author=request.user, type=2)
            new_activity.save()
            ###Profile.objects.filter(user=request.user).update(date_active=timezone.now)

            if(tagfield):
                #Tag filtering
                try:
                    tag_dict = tagfield.split()
                    for tag in tag_dict:
                        if(tag.startswith("#")):
                            try:
                                try:
                                    topic = Topic.objects.get(title=tag[1:])
                                    new_post.topics.add(topic)
                                except:
                                    topic = Topic(title=tag[1:])
                                    topic.save()
                                    new_post.topics.add(topic)
                            except Exception as e:
                                new_post.content = e

                        elif(tag.startswith("@")):
                            try:
                                try:
                                    person = User.objects.get(username=tag[1:])
                                    new_post.people.add(person)
                                    new_notification = Notification(sender=request.user, recepient=person, post=new_post, type=2)
                                    if(new_notification.sender != new_notification.recepient):
                                        new_notification.save()
                                except Exception as e:
                                    print(f"____________________________{e}")
                            except Exception as e:
                                print(f"____________________________{e}")

                except:
                    pass
    return render(request, 'blog/search_results.html', context)

def getTopic(request, topic=None):
    page_limit = 10
    post_form = NewPostForm()
    posts = Post.objects.filter(topics__title=topic).annotate(count=Count('like')).order_by('-count')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, page_limit)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    today = datetime.datetime.now()
    #Get all tags
    tops = Topic.objects.filter(post__topics__title=topic).annotate(count=Count('post__like')).order_by('-count')
    peps = User.objects.filter(post__topics__title=topic).annotate(count=Count('post__like')).order_by('-count')

    acts = Activity.objects.filter(post__date_posted__day=today.day, post__topics__title=topic).order_by('-date')
    last_acts = Activity.objects.filter(post__topics__title=topic).last()

    context = {
            'posts': posts,
            'profile': request.user.profile,
            'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
            'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
            'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
             Notification.objects.filter(recepient=request.user, confirmed=False).count(),
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'likes' : Like.objects.all(),
            'activities' : acts,
            'activities_last' : last_acts,
            'user' : request.user,
            'obj' : Post.objects.get(id=10),
            'post_form' : post_form,
            'people' : peps,
            'topics' : tops,
            'date' : today,
            'page_limit' : page_limit,
            'topic' : topic,
            'topic_count' : Post.objects.filter(topics__title=topic).order_by('date_posted').count(),
            'topic_likes' : Like.objects.filter(post__topics__title=topic).order_by('date_posted').count(),
            'topic_users' : Profile.objects.filter(user__post__topics__title=topic).annotate(count=Count('user')).order_by('-count').distinct().count(),
            'topic_first_post' : Post.objects.filter(topics__title=topic).order_by('date_posted').first(),
            'topic_best_post' : Post.objects.filter(topics__title=topic).annotate(count=Count('like')).order_by('-count').first(),
            }

#When user clicks on a post
    if request.is_ajax():
        if(request.POST.get('id')):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
        else:
            post_id = 10
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
            'activities_last' : last_acts,
            'post_form' : post_form,
            'page_limit' : page_limit,
            'slice_custom' : page_limit,
            'topic' : topic,
            'topic_first_post' : Post.objects.filter(topics__title=topic).order_by('date_posted').first(),
            'topic_best_post' : Post.objects.filter(topics__title=topic).order_by('like').first(),
            }

        if (request.POST.get('action') == "Comment"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            cont = request.POST.get('content')
            post = Post.objects.get(id=request.POST.get('id'))
            author = request.user
            post = Post(content=cont,author=author, reply=post)
            post.save()
            new_activity = Activity(post=obj, author=request.user, type=1)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_activity = Activity(post=post, author=request.user, type=2)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=post, type=1)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            html3 = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2, 'post' : html3})

        elif (request.POST.get('action') == "View_Post"):
            html = render_to_string('blog/post.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "View_Content"):
            html = render_to_string('blog/content_view.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Like_Post"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html = render_to_string('blog/post_like_comment.html', sub_context, request=request)
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Post_Reply"):
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
                    new_activity = Activity.objects.filter(post=obj, author=request.user, type=0)
                    new_activity.delete()
                    new_notification = Notificationobjects.filter(sender=request.user, recepient=obj.author, post=obj, type=0)
                    new_notification.delete()
            except:
                pass
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html, 'main' : html2})

        elif (request.POST.get('action') == "Like_Feed"):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
            post = Post.objects.get(id=request.POST.get('id'))
            like = None
            try:
                likes = Like.objects.filter(post=post, author=request.user)
                if(not likes):
                    new_like = Like(post=post,author=request.user)
                    new_like.save()
                    new_activity = Activity(post=obj, author=request.user, type=0)
                    new_activity.save()
                    ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
                    new_notification = Notification(sender=request.user, recepient=obj.author, post=obj, type=0)
                    if(new_notification.sender != new_notification.recepient):
                        new_notification.save()
                else:
                    likes.delete()
            except:
                pass

            sub_context['replies'] = Post.objects.filter(reply=obj.reply)
            html = render_to_string('blog/feed.html', sub_context, request=request)
            sub_context["p"] = Post.objects.get(id=request.POST.get('id'))
            html2 = render_to_string('blog/like_comment.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2})

        elif (request.POST.get('action') == "New_Post"):
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Delete_Post"):

            post = Post.objects.get(id=post_id)
            post.delete()
            html3 = render_to_string('blog/replies.html', sub_context, request=request)
            html2 = render_to_string('blog/feed.html', sub_context, request=request)
            html = render_to_string('blog/post.html', sub_context, request=request)
            return JsonResponse({'form':html,'main':html2,'post':html3})

        elif (request.POST.get('action') == "Repost"):

            post = Post.objects.get(id=post_id)
            repost = Post(author=request.user, reply=None, repost=post)
            repost.save()
            new_activity = Activity(post=Post.objects.get(id=post_id), author=request.user, type=3)
            new_activity.save()
            ##Profile.objects.filter(user=request.user).update(date_active=timezone.now)
            new_notification = Notification(sender=request.user, recepient=obj.author, post=repost, type=3)
            if(new_notification.sender != new_notification.recepient):
                new_notification.save()
            html = render_to_string('blog/feed.html', sub_context, request=request)
            return JsonResponse({'form':html})

        #User Actions

        elif (request.POST.get('action') == "Open_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Notifications"):
            notifications = Notification.objects.filter(recepient=request.user)
            notifications.delete()
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Open_Requests"):
            requests = Request.objects.filter(recepient=request.user, confirmed=False).update(confirmed=True)
            html = render_to_string('blog/notifications_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Clear_Requests"):
            requets = Request.objects.filter(recepient=request.user)
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Decline_Request"):
            requets = Request.objects.get(id=request.POST.get('request_id'))
            requets.delete()
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return JsonResponse({'form':html})

    #Site Behaviour
        elif (request.POST.get('action') == "Load_Next"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/feed.html',new_context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Load_Next_Reply"):
            page_count = request.POST.get('page_count')
            new_context = sub_context
            new_context["page_limit"] += int(page_count)
            html = render_to_string('blog/replies.html',new_context, request=request)
            return JsonResponse({'form':html})

    elif (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES)
        if(post_form.is_valid()):
            tagfield = post_form.cleaned_data.get('tags')
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user, reply=None)

            #Media filtering
            try:
                media = request.FILES['media']
                url = media.name.lower()
                if (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png')):
                    new_post.image = media
                elif (url.endswith('.mp4') or url.endswith('.ogg') or url.endswith('.webm')):
                    new_post.video = media
            except:
                pass

            new_post.save()
            post_form = NewPostForm()

            new_activity = Activity(post=new_post, author=request.user, type=2)
            new_activity.save()
            ###Profile.objects.filter(user=request.user).update(date_active=timezone.now)

            if(tagfield):
                #Tag filtering
                try:
                    tag_dict = tagfield.split()
                    for tag in tag_dict:
                        if(tag.startswith("#")):
                            try:
                                try:
                                    topic = Topic.objects.get(title=tag[1:])
                                    new_post.topics.add(topic)
                                except:
                                    topic = Topic(title=tag[1:])
                                    topic.save()
                                    new_post.topics.add(topic)
                            except Exception as e:
                                new_post.content = e

                        elif(tag.startswith("@")):
                            try:
                                try:
                                    person = User.objects.get(username=tag[1:])
                                    new_post.people.add(person)
                                    new_notification = Notification(sender=request.user, recepient=person, post=new_post, type=2)
                                    if(new_notification.sender != new_notification.recepient):
                                        new_notification.save()
                                except Exception as e:
                                    print(f"____________________________{e}")
                            except Exception as e:
                                print(f"____________________________{e}")

                except:
                    pass

    return render(request, 'blog/topic_posts.html', context)

def get_user_information(request, username=None, view=None):
    page_limit = 10
    profile = Profile.objects.get(user__username=username)
    #Profile information is accquired here.

    post_form = NewPostForm()
    posts = Post.objects.filter(Q(author=profile.user) | Q(people=profile.user)).order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    today = datetime.datetime.now()
    from django.db.models import Count

    #Get all tags
    tops = Topic.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')
    peps = User.objects.filter(post__date_posted__day=today.day).annotate(count=Count('post__like')).order_by('-count')

    acts = Activity.objects.filter(author=profile.user).order_by('-date')


    from django.db import models
    #Get page filters
    circles = Profile.objects.all()
    img = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    if(view == "media"):
        posts = Post.objects.filter(Q(author__username=profile.user.username) & Q(~Q(image="default.jpg") | ~Q(video=""))).order_by('-date_posted')
    elif(view == "friends"):
        circles = Profile.objects.filter(Q(friends=profile)).order_by('-id')
    elif(view == "followers"):
        circles = Profile.objects.filter(Q(following=profile)).order_by('-id')
    elif(view == "following"):
        circles = Profile.objects.filter(Q(followers=profile))
    elif(view == "replies"):
        posts = Post.objects.filter(Q(author=profile.user) & ~Q(reply=None)).order_by('-date_posted')
    elif(view == "likes"):
        posts = Post.objects.filter(Q(like__author=profile.user)).order_by('-date_posted')
    elif(view == "feed"):
        posts = Post.objects.filter(Q(author=profile.user)).order_by('-date_posted')

    #Get Profile accquaintences

    def isFriend():
        try:
            return (not profile.friends.get(user=request.user) == None)
        except:
            return False

    def isFollowing():
        try:
            return (not profile.followers.get(user=request.user) == None)
        except:
            return False

    def isRequestExists():
        try:
            return (Request.objects.get(recepient=profile.user,sender=request.user) != None)
        except:
            return False

    context = {
        'posts': posts,
        'pages': pages,
        'followers_count' : profile.followers.count(),
        'following_count' : profile.following.count(),
        'friends_count' : profile.friends.count(),
        'page_obj':paginator,
        'profile': profile,
        'comments' : Comment.objects.all(),
        'likes' : Like.objects.all(),
        'user' : request.user,
        'activities' : acts,
        'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
        'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
        'existing_request' : isRequestExists(),
        'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
        Notification.objects.filter(recepient=request.user, confirmed=False).count(),
        'media' : Post.objects.filter(Q(author=profile.user) & ~Q(image="default.jpg", author=profile.user) | ~Q(video="")).order_by('-date_posted'),
        'user_posts' : Post.objects.filter(author__username=username).order_by('-date_posted').count(),
        'user_comments' : Post.objects.filter(reply__author__username=username).order_by('-date_posted').count(),
        'obj' : Post.objects.get(id=3),
        'user_likes' : Like.objects.filter(author__username=username).order_by('-date_posted').count(),
        'post_form' : post_form,
        'people' : peps,
        'topics' : tops,
        'date' : today,
        'page_limit' : page_limit,
        #Functions
        'is_friend' : isFriend(),
        'is_following' : isFollowing(),
        'view' : view,
        'circles' : circles,
        }

    if request.is_ajax():
        if(request.POST.get('id')):
            post_id = request.POST.get('id')
            obj = Post.objects.get(id=post_id)
        else:
            post_id = 10
            obj = Post.objects.get(id=post_id)


        sub_context = {
            'posts': posts,
            'profile': profile,
            'page_obj': paginator,
            'pages' : pages,
            'comments' : Comment.objects.all(),
            'replies' : Post.objects.filter(reply=obj),
            'replies-reply' : Post.objects.filter(reply=obj),
            'likes' : Like.objects.all(),
            'user' : request.user,
            'obj' : obj,
            'media' : Post.objects.filter(Q(author__username=username) & ~Q(image="default.jpg") | ~Q(video="")).order_by('-date_posted'),
            'activities' : Activity.objects.filter(post=Post.objects.get(id=post_id)),
            'post_form' : post_form,
            'page_limit' : page_limit,
            #Functions
            'is_friend' : isFriend(),
            'is_following' : isFollowing(),
            'view' : view,
            'circles' : circles,
            }

        if (request.POST.get('action') == "Follow"):
            if(isFollowing()):
                request.user.profile.following.remove(profile)
            else:
                request.user.profile.following.add(profile)
                new_notification = Notification(sender=request.user, recepient=profile.user, type=4)
                if(new_notification.sender != new_notification.recepient):
                    new_notification.save()
            html = render_to_string('blog/profile_overhead.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Send_Request"):
            request = Request(sender=request.user, recepient=profile.user)
            request.save()
            html = render_to_string('blog/profile_overhead.html', context, request=request)
            return JsonResponse({'form':html})

        elif (request.POST.get('action') == "Unfriend"):
            request.user.profile.friends.remove(profile)
            html = render_to_string('blog/profile_overhead.html', context, request=request)
            return JsonResponse({'form':html})

    #Site Behaviour
        elif (request.POST.get('action') == "Load_Next"):
                page_count = request.POST.get('page_count')
                new_context = sub_context
                new_context["page_limit"] += int(page_count)

                if(view == "friends" or view == "followers" or view == "following"):
                    html = render_to_string('blog/feed_circles.html',new_context, request=request)
                else:
                    html = render_to_string('blog/feed.html',new_context, request=request)

                return JsonResponse({'form':html})

    elif (request.method == 'POST'):
        post_form = NewPostForm(request.POST, request.FILES)
        if(post_form.is_valid()):
            tagfield = post_form.cleaned_data.get('tags')
            con = post_form.cleaned_data.get('content')
            new_post = Post(content=con, author=request.user, reply=None)

            #Media filtering
            try:
                media = request.FILES['media']
                url = media.name.lower()
                if (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png')):
                    new_post.image = media
                elif (url.endswith('.mp4') or url.endswith('.ogg') or url.endswith('.webm')):
                    new_post.video = media
            except:
                pass

            new_post.save()
            post_form = NewPostForm()

            if(tagfield):
                #Tag filtering
                try:
                    tag_dict = tagfield.split()
                    for tag in tag_dict:
                        if(tag.startswith("#")):
                            try:
                                try:
                                    topic = Topic.objects.get(title=tag[1:])
                                    new_post.topics.add(topic)
                                except:
                                    topic = Topic(title=tag[1:])
                                    topic.save()
                                    new_post.topics.add(topic)
                            except Exception as e:
                                new_post.content = e

                        elif(tag.startswith("@")):
                            try:
                                try:
                                    person = User.objects.get(username=tag[1:])
                                    new_post.people.add(person)
                                except Exception as e:
                                    print(f"____________________________{e}")
                            except Exception as e:
                                print(f"____________________________{e}")

                except:
                    pass

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
