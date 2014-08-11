from Agora.forms import *
from Agora.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/newuser/')
    else:
        form = registrationForm()
    body = RequestContext(request, {'form': form })
 
    return render_to_response('register.html', body,)
 
def newuser(request):
    if request.methog == "POST":
        form = profileForm(request.POST)
        if form.is_valid():
            p = profiles(
                user=request.user,
                blur=form.blur,
                photo=form.photo,
                role=form.role)
            p.save()
            try:
                user = User.objects.get(username=request.user)
            except User.DoesNotExist:
                return HttpResponseRedirect('/login/')
            else:
                user.first_name = form.firstname
                user.last_name = form.surname
                user.save()
            return HttpResponseRedirect('/'+request.user+'/')
    else:
        form = profileForm()

    body = RequestContext(request, {'form' : form })
    return render_to_response('newuser.html', body,)
 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response('home.html',{ 'user': request.user })

