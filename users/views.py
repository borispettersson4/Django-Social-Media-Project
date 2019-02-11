from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from blog.models import *
from PIL import Image
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your views here.
def register(request):

    if(request.method == 'POST'):
        form = UserRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your Account Has Been Created. Sign In To Get Started, {username}!")
            try:
                new_settings = ProfileSettings(user=request.user)
                new_settings.save()
            except:
                pass

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form, 'title':'Register'})

@login_required
def profile(request):
    if (request.method == 'POST'):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        profile_form = ProfileNickUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        profileSettings_form = ProfileSettingsUpdateForm(request.POST, request.FILES, instance=request.user.profilesettings)

        if (u_form.is_valid() and p_form.is_valid() and profile_form.is_valid() and profileSettings_form.is_valid()):
            u_form.save()
            p_form.save()
            profile_form.save()
            cover = profileSettings_form.cleaned_data.get('coverImage')
            profileSettings_form.save()
            ps = request.user.profilesettings
            ps = ProfileSettings(user=ps.user,about=ps.about, quote=ps.quote, coverImage=cover, id=ps.id)
            ps.save()
            messages.success(request, f"Your Account Has Been Updated!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        profile_form = ProfileNickUpdateForm(instance=request.user.profile)
        profileSettings_form = ProfileSettingsUpdateForm(instance=request.user.profilesettings)

    context = {
    'u_form' : u_form,
    'p_form' : p_form,
    'profile_form' : profile_form,
    'profileSettings_form' : profileSettings_form,
    'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
    'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
    'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
    Notification.objects.filter(recepient=request.user, confirmed=False).count(),
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

    return render(request, 'users/profile.html', context)

@login_required
def feedback(request):
    if (request.method == 'POST'):
        form = FeedbackForm(request.POST, instance=request.user)
        if (form.is_valid()):
            form.save()

            op1 = form.cleaned_data.get('quality_speed')
            op2 = form.cleaned_data.get('quality_features')
            op3 = form.cleaned_data.get('quality_visual')
            op4 = form.cleaned_data.get('quality_stability')
            op5 = form.cleaned_data.get('quality_responsiveness')
            op6 = form.cleaned_data.get('comment')

            feedback = Feedback(quality_speed=op1,quality_features=op2,quality_visual=op3,quality_stability=op4
            ,quality_responsiveness=op5,comment=op6, author=request.user)
            feedback.save()

            messages.success(request, f"Your feedback has been sent.")
            return redirect('feedback-sent')

    else:
        form = FeedbackForm(instance=request.user)

    context = {
    'form' : form,
    'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
    'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
    'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
    Notification.objects.filter(recepient=request.user, confirmed=False).count(),
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/feedback.html', context)

@login_required
def feedback_sent(request):

    context = {
    'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
    'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
    'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
    Notification.objects.filter(recepient=request.user, confirmed=False).count(),
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/feedback_sent.html', context)

def about(request):

    context = {

    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/about.html', context)

@login_required
def privacy(request):

    context = {
    'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
    'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
    'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
    Notification.objects.filter(recepient=request.user, confirmed=False).count(),
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/privacy.html', context)

def terms_of_service(request):

    context = {
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/terms_of_service.html', context)

@login_required
def legal(request):

    context = {
    'notifications' : Notification.objects.filter(recepient=request.user).order_by('-date_posted'),
    'requests' : Request.objects.filter(recepient=request.user).order_by('-date_posted'),
    'badge_count' : Request.objects.filter(recepient=request.user, confirmed=False).count() +
    Notification.objects.filter(recepient=request.user, confirmed=False).count(),
    'hide_post' : True,
    }

    if request.is_ajax():
        if (request.POST.get('action') == "Open_Notifications"):
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

        elif (request.POST.get('action') == "Accept_Request"):
            request_obj = Request.objects.get(id=request.POST.get('request_id'))
            request.user.profile.friends.add(request_obj.sender.profile)
            html = render_to_string('blog/requests_view.html', context, request=request)
            return render(request, 'users/feedback.html', context)

    return render(request, 'users/legal.html', context)
