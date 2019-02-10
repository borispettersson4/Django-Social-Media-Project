from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
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
    'profileSettings_form' : profileSettings_form
    }

    return render(request, 'users/profile.html', context)
