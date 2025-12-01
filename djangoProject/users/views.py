from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import AuthUserForm, UserRegistrationForm, UserUpdateForm


class Login(LoginView):
    fields = ["username", "password"]
    template_name = 'users/login.html'
    form_class = AuthUserForm


class Logout(LogoutView):
    template_name = 'users/logout.html'


def register(request):
    regform = UserRegistrationForm(request.POST)
    if request.method == "POST":
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_active = True
            reg_f.is_staff = False
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.date_login = datetime.now()
            regform.save()

            reg_f.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, reg_f)
            return redirect('news:index')
    else:
        regform = UserRegistrationForm()
    return render(request, 'users/registration.html', {'regform': regform})

def profile(request):
    user = request.user.news_set.all()
    return render(request, 'users/profile.html', {'user_news': user})


def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})