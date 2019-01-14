from django.shortcuts import render
from django.http import HttpResponse

#Dummy Database
posts = [
    {
        'author':'A Person',
        'title':'The Red Horse',
        'content':'Example content',
        'date_posted':'January 20, 2019'
    },
    {
        'author':'Another Persone',
        'title':'The Blue River',
        'content':'Example content 2',
        'date_posted':'January 21, 2019'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

def login(request):
    return render(request, 'blog/login.html', {'title':'Log In'})

def register(request):
    return render(request, 'blog/register.html', {'title':'Register'})
