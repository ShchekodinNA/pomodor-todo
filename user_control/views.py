from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UpdatedUserRegistrationForm
# Create your views here.


def register_request(request):
    if request.method == 'POST':
        form = UpdatedUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration is completed successfully')
            return redirect('home')
        messages.error(
            request, 'Unsuccessful registration. Invalid information')
        return render(request=request, template_name='user_control/register.html', context={'register_form': form})
    form = UpdatedUserRegistrationForm()
    return render(request=request, template_name='user_control/register.html', context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request=request, template_name='user_control/login.html', context={'login_form': form})
    form = AuthenticationForm()
    return render(request=request, template_name='user_control/login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
