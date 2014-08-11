from Agora.forms import *
from Agora.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext

 
@csrf_protect
def register(request):
    """
    This is the user register commands so when they create an account this will pop up.
    :param request: this translate into the POST request of the user and password
    :return: either a form to login to or the next page to add info
    """
    if request.method == 'POST':
        form = registrationForm(request.POST)
        # checks if the form data is valid if so then adds the user to the database.
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            # this then logs the user into the system
            loginUser = authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
            login(request,loginUser)
            # send them to the next page of the registration.
            return HttpResponseRedirect('/newuser/')
    else:
        form = registrationForm()
    body = RequestContext(request, {'form': form })
 
    return render_to_response('register.html', body,)

@login_required(login_url='/login/')
def newuser(request):
    """
    This page is to add more personal information about the user here.
    :param request:  is another form to add their details
    :return: either an empty form or sends them to their profile page.
    """
    if request.method == "POST":
        form = profileForm(request.POST, request.FILES)
        # checks to see if the user form is filled in correctly
        if form.is_valid():
            # checks if there is that user if there isn't they get sent away
            try:
                usera = User.objects.get(username=request.user)
            except User.DoesNotExist:
                return HttpResponseRedirect('/login/')
            else:
                # this adds the profile information to the database
                p = Profiles(
                user = usera.id,
                blur = form.cleaned_data['aboutme'],
                photo = form.cleaned_data['photo'],
                role = form.cleaned_data['role'],
                )
                p.save()

                usera.first_name = form.cleaned_data['firstname']
                usera.last_name = form.cleaned_data['surname']
                usera.save()
            return HttpResponseRedirect('/'+request.user.username+'/')
    else:
        form = profileForm()

    body = RequestContext(request, {'form' : form })
    return render_to_response('newuser.html', body,)


def logout_view(request):
    """
    This logs the individual out of the system
    :return: Sends them to the home page.
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def home(request):
    """
    The home page, if the user is logged in then they get sent to their user page else a login page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/'+request.user.username+'/')
    else:
        return HttpResponseRedirect('/');

@login_required(login_url='/login/')
def profile(request, username):
    """
    This creates a profile page for each user, based on their username.
    So each page will be populated by that user's information
    """
    user = User.objects.get(username=username)
    prof= Profiles.objects.get(user=user.id)
    repo = None
    return render(request, 'user.html',{'user':user, 'prof':prof, 'repo':repo})

def frontpage(request):
    """
    The frontpage of the whole project
    """
    return render(request, 'frontpage.html',{'note':"hello"})