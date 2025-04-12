from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from ..utils import clean_email, clean_password, clean_username


class Login(View):
    def get(self, request, template_name='login.html'):
        return render(request, template_name)

    def post(self, request, template_name='login.html'):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.add_message(
            request, constants.ERROR, "Usuário ou senha inválidos"
        )
        return render(request, template_name)


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request, template_name='signup.html'):
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        try:
            clean_username(username)
            clean_password(password)
            clean_email(email)
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            return redirect('login')
        except ValidationError as err:
            messages.add_message(request, constants.ERROR, str(err))
        return render(request, template_name)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
