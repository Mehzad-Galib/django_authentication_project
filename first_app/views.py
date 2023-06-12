from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, render

from .forms import ChangeUserData, RegisterForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')
            messages.warning(request, 'warning')
            messages.info(request, 'info')
            form.save()
            print(form.cleaned_data)
    else:
        form = RegisterForm()
    return render(request, './signup.html', {'form': form })


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username = name, password = userpass) # checking if user belongs to DB
                
                if user is not None:
                    login(request, user)
                    print(user)
                    return redirect('profile')
            
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('profile')
    
def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeUserData(request.POST, instance = request.user)
            if form.is_valid():
                messages.success(request, 'Account updated successfully')
                form.save()
        else:
            form = ChangeUserData(instance = request.user)
        return render(request, './profile.html', {'form': form })
    else:
        return redirect('signup')

def user_logout(request):
    logout(request)
    return redirect('login')

def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                # update_session_auth_hash(request, form.cleaned_data['user']) # it will update password
                return redirect('profile')
            
        else:
            form = PasswordChangeForm(user=request.user)
            
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')
    
    
    
def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeUserData(request.POST, instance = request.user)
            if form.is_valid():
                messages.success(request, 'Account updated successfully')
                form.save()
        else:
            form = ChangeUserData(instance = request.user)
        return render(request, './update_profile.html', {'form': form })
    else:
        return redirect('signup')
    