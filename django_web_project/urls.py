from django.contrib import admin
from django.conf.urls import include
from django.urls import include, path
from django.contrib.auth import views as auth_views
from users import views as user_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super-auth', admin.site.urls),
    path('register/', user_views.register,name='register'),
    path('profile/', user_views.profile,name='profile'),
    path('feedback/', user_views.feedback,name='feedback'),
    path('about/', user_views.about,name='about'),
    path('privacy/', user_views.privacy,name='privacy'),
    path('legal/', user_views.legal,name='legal'),
    path('welcome/', user_views.welcome,name='welcome'),
    path('terms_of_service/', user_views.terms_of_service,name='terms_of_service'),
    path('feedback/sent', user_views.feedback_sent,name='feedback-sent'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('', include('blog.urls')),
]

if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
