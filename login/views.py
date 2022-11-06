from django.shortcuts import render, redirect
from . import urls



def login(request):
    return render(request=request, template_name='login.html',)


def logout(request):
    return render(request=request, template_name='logout.html')


def signup(request):
    return render(request=request, template_name='signup.html')