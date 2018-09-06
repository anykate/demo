from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MyUserLoginForm, MyUserRegistrationForm

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)


# Create your views here.
@login_required(login_url='myaccounts:login')
def home(request):
    return render(request, 'myaccounts/home.html', {})


def login_view(request):
    next = request.GET.get('next')
    form = MyUserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('myaccounts:home')
    return render(request, 'myaccounts/login.html', {'form': form})


def registration_view(request):
    if not request.user.is_authenticated:
        next = request.GET.get('next')
        form = MyUserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email1')
            user.set_password(password)
            user.email = email
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('myaccounts:home')
        return render(request, 'myaccounts/signup.html', {'form': form})
    else:
        return redirect('myaccounts:home')


@login_required(login_url='myaccounts:login')
def logout_view(request):
    logout(request)
    return redirect('myaccounts:home')
