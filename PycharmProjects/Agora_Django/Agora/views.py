from Agora.forms import *
from Agora.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Agora_git import functions
from Agora_git.models import *
import json
import time
from Agora_Django import settings
import os

 
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
                    user = usera,
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
        return HttpResponseRedirect('/')



@login_required(login_url='/login/')
def profile(request, username):
    """
    This creates a profile page for each user, based on their username.
    So each page will be populated by that user's information
    """
    user = User.objects.get(username=request.user)
    prof= Profiles.objects.get(user=user.id)
    try:
        repolist = Repository.objects.filter(user=user)
    except Repository.DoesNotExist:
        return render(request, 'user.html',{'user':user, 'prof':prof })
    else:
        #for item in repolist:
         #   item.name = item.name.replace("_"," ")

        return render(request, 'user.html',{'user':user, 'prof':prof, 'repolist':repolist})



def frontpage(request):
    """
    The frontpage of the whole project
    """
    return render(request, 'frontpage.html',{'note':"hello"})



@login_required(login_url='/login/')
def CreateRepoForUser(request,username):
    """
    This will set up the form for a new project(repo) for the user to add work to
    :param request:  normal request
    :param username: user name of where the project will be connected to.
    :return:
    """
    if username == request.user.username:
        if request.method == "POST":
            form = NewRepoForm(request.POST)

            if form.is_valid():
                namerepo = form.cleaned_data['reponame']
                if functions.create_repo(namerepo):
                    functions.user_repo(namerepo,request.user)
                    return HttpResponseRedirect('/'+request.user.username+'/'+namerepo)
                else:
                    errormesg = "Could not create a new project for some reason, possilbe one already exists."
                    return HttpResponseRedirect("/error/"+errormesg.replace(" ","_"))
        else:
            form = NewRepoForm()
        body = RequestContext(request, {'form' : form })
        return render_to_response('createrepo.html', body,)
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')



def repoProject(request,username,project):
    path = os.path.join(settings.REPO_ROOT,project)
    result = []
    result += [ file for file in os.listdir(path) if file.endswith('.note')]
    data = []
    for file in result:
        f = open(os.path.join(path,file),'r')
        info = json.loads(f.read())
        d ={}

        d['name']=file[0:-5]
        d['user']=info['note']['user']
        d['content']=info['note']['content']
        d['type']=info['note']['type']

        data.append(d)

    if request.user.username == username:
        # make the project editable
        body = {'usera':username, 'file': data}
    else:
        # can't be edited just viewed
        body = {'file': data}
    return render(request, 'project.html',body)



@login_required(login_url='/login/')
def new_note(request,username,project):
    repo = Repository.objects.get(name__iexact=project,user__iexact=request.user.id)

    if True:
        if request.method == "POST":
            noteform = NoteForm(request.POST)

            if noteform.is_valid():
                # create the json here on the temp dir

                jsonfile = json.dumps({"note":{
                    "user":request.user.username,
                    "datetime": int(time.time()),
                    "type":"html",
                    "content": noteform.cleaned_data['content'],
                    "bg": noteform.cleaned_data['bg_colour'],
                    "tx": noteform.cleaned_data['tx_colour'],
                },"comment":{}})
                filename = u"{date}{user}server.note".format(date=int(time.time()),user=request.user.username)
                output = open(os.path.join(settings.REPO_ROOT,project,filename),'w')
                output.write(jsonfile)
                output.close()
                if functions.add_file(project,filename):
                    return HttpResponseRedirect("/"+username+"/"+project)

                else:
                    errormesg = "Couldn't add note to the repository."
                    return HttpResponseRedirect("/error/"+errormesg.replace(" ","_"))



        else:
            noteform = NoteForm()

        body = RequestContext(request, {'Noteform' : noteform})
        return render_to_response('createnote.html',body)
    else:
        errormesg = "You don't have access to this project to add notes."
        return HttpResponseRedirect("/error/"+errormesg.replace(" ","_"))



def error(request,mesg):
    body = {"mesg":mesg.replace("_"," ")}
    return render(request,'error.html',body)


def view_note(request, username, project, note):
    path = os.path.join(settings.REPO_ROOT,project,note)
    f = open(path+".note",'r')
    info = json.loads(f.read())
    body ={}
    body['name']=note
    body['user']=info['note']['user']
    body['content']=info['note']['content']
    body['type']=info['note']['type']
    print body
    return render_to_response('view_note.html',body)