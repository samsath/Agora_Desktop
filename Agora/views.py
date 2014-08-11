from Agora.forms import *
from Agora.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
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
    if request.method == "POST":
        form = profileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                userd = request.user
            except User.DoesNotExist:
                return HttpResponseRedirect('/login/')
            else:
                p = Profiles(
                user = userd,
                blur = form.cleaned_data['aboutme'],
                photo = form.cleaned_data['photo'],
                role = form.cleaned_data['role'],
                )
            p.save()
            try:
                usera = User.objects.get(username=request.user)
            except User.DoesNotExist:
                return HttpResponseRedirect('/login/')
            else:
                usera.first_name = form.cleaned_data['firstname']
                usera.last_name = form.cleaned_data['surname']
                usera.save()
            return HttpResponseRedirect('/'+request.user.username+'/')
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


def profile(request, username):
    user = User.objects.get(username=username)
    prof= Profiles.objects.get(user=user.id)
    repo = None
    return render(request, 'user.html',{'user':user, 'prof':prof, 'repo':repo})