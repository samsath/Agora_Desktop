from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm

def login_view(request, template_name):
    """
    This is a login view so allow people to log into the website
    :param request:
    :return:to the user's account or to an invalid username page.
    """
    username = request.POST.get('username','')
    password = request.POST.get('password','')

    user = auth.authenticate(username=username,password=password)
    if user is not None and user.is_active:
        auth.login(request,user)

        return HttpResponseRedirect("/"+username+"/")
    else:
        return render(request, 'invalid.html',{'reason':"Not able to log in, information provided is wrong"})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/newuser/")
        else:
            form = UserCreationForm()
        return render(request, "register.html", {'form':form,})