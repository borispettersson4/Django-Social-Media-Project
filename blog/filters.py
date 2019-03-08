from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from users.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
from django.db.models import Q

register = template.Library()

@register.filter
def has_comment(post,user):
    return post.comment_set.filter(author=user)

@register.filter
def has_reply(post,user):
    return post.post_set.filter(Q(author=user))

@register.filter
def get_comment_set(post,user):
    return post.post_set.filter(Q(author=user) & ~Q(reply=post)).count()

@register.filter
def set_value(variable,value):
    request.session['post_id'] = value
    return None

@register.filter
def has_like(post,user):
    return post.like_set.filter(author=user)

@register.filter
def get_message_content(profile, user):
    try:
        rec_msg = profile.user.msgrecepient.filter(Q(sender=user)).last()
    except:
        rec_msg = ""
    try:
        sen_msg = profile.user.msgsender.filter(Q(recepient=user)).last()
    except:
        sen_msg = ""

    if(sen_msg and rec_msg):
        return rec_msg.content if rec_msg.date_posted > sen_msg.date_posted else sen_msg.content
    elif(sen_msg):
        return sen_msg.content
    elif(rec_msg):
        return rec_msg.content
    else:
        return ""

@register.filter
def get_message_last(profile, user):
    try:
        rec_msg = profile.user.msgrecepient.filter(Q(sender=user)).last()
    except:
        rec_msg = ""
    try:
        sen_msg = profile.user.msgsender.filter(Q(recepient=user)).last()
    except:
        sen_msg = ""

    if(sen_msg and rec_msg):
        return rec_msg if rec_msg.date_posted > sen_msg.date_posted else sen_msg
    elif(sen_msg):
        return sen_msg
    elif(rec_msg):
        return rec_msg
    else:
        return ""

@register.filter
def get_messages_unconfirmed(profile, user):
    return(Message.objects.filter(recepient=user, sender=profile.user, confirmed=False))


@register.filter
def get_message_last_date(profile, user):
    try:
        rec_msg = profile.user.msgrecepient.filter(Q(sender=user)).last()
    except:
        rec_msg = ""
    try:
        sen_msg = profile.user.msgsender.filter(Q(recepient=user)).last()
    except:
        sen_msg = ""

    if(sen_msg and rec_msg):
        return rec_msg.date_posted if rec_msg.date_posted > sen_msg.date_posted else sen_msg.date_posted
    elif(sen_msg):
        return sen_msg.date_posted
    elif(rec_msg):
        return rec_msg.date_posted
    else:
        return ""

#User Posts Profile

@register.filter
def is_friends(user,friend):
    return (user.profile.friends.get(friend) == None)

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""

@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])

@register.filter("slice_custom", is_safe=True)
def slice_filter(value, arg):
    try:
        bits = []
        for x in arg.split(':'):
            if len(x) == 0:
                bits.append(None)
            else:
                bits.append(int(x))
        return value[slice(*bits)]

    except (ValueError, TypeError):
        return value # Fail silently.
