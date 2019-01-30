from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from users.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from chartjs import *
from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
register = template.Library()

@register.filter
def has_comment(post,user):
    return post.comment_set.filter(author=user)

@register.filter
def has_reply(post,user):
    return post.post_set.filter(author=user)

@register.filter
def set_value(variable,value):
    request.session['post_id'] = value
    return None

@register.filter
def has_like(post,user):
    return post.like_set.filter(author=user)

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
