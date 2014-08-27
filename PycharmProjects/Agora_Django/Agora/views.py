from django.forms.formsets import formset_factory
from Agora.forms import *
from Agora.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
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


@csrf_protect
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

@csrf_protect
@login_required(login_url='/login/')
def home(request):
    """
    The home page, if the user is logged in then they get sent to their user page else a login page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/'+request.user.username+'/')
    else:
        return HttpResponseRedirect('/')


@csrf_protect
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
        data = []
        for item in repolist:
            path = os.path.join(settings.REPO_ROOT,item.name)
            result = []
            result += [ file for file in os.listdir(path) if file.endswith('.note')]

            for file in result:
                f = open(os.path.join(path,file),'r')
                info = json.loads(f.read())
                d ={}

                d['name']=item.name+"/"+file[0:-5]
                d['user']=info['note']['user']
                d['content']=info['note']['content']
                d['tx']=info['note']['tx']
                d['bg']=info['note']['bg']

                data.append(d)
            #item.name = item.name.replace("_"," ")

        return render(request, 'user.html',{'user':user, 'prof':prof, 'repolist':repolist,'file': json.dumps(data)})



@csrf_protect
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

@csrf_protect
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
        d['tx']=info['note']['tx']
        d['bg']=info['note']['bg']

        data.append(d)

    if request.user.username == username:
        # make the project editable
        repo = Repository.objects.get(name=project).hashurl
        link = settings.DOMAIN+"/add/user/"+repo


        body = {'usera':username, 'file': json.dumps(data),'repo':project,'reponame':project.replace("_"," "),'link':link}
    else:
        # can't be edited just viewed
        body = {'file': json.dumps(data),'repo':project,'reponame':project.replace("_"," ")}
    return render(request, 'project.html',body)


@csrf_protect
@login_required(login_url='/login/')
def new_note(request,username,project):
    repo = Repository.objects.get(name__contains=project,user=request.user)

    if(repo is not 0):
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
                },"comment":[]})
                filename = u"{date}{user}server.note".format(date=int(time.time()),user=request.user.username)
                output = open(os.path.join(settings.REPO_ROOT,project,filename.lower()),'w')
                output.write(jsonfile)
                output.close()
                #if functions.add_file(project,filename):
                return HttpResponseRedirect("/"+username+"/"+project)



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


@csrf_protect
def view_note(request, username, project, note):
    nname = note
    body ={}
    body.update(csrf(request))
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        body['user']=user

    path = os.path.join(settings.REPO_ROOT,project,note)
    f = open(path+".note",'r')
    info = json.loads(f.read())
    f.close()

    comments=[]
    for com in info['comment']:
        comment={}
        comment['user']=com['user']
        comment['body']=com['body']
        comments.append(comment)
    body['comments']=comments

    repo = Repository.objects.get(name=project).hashurl
    link = settings.DOMAIN+"/add/user/"+repo
    body['link']=link

    if request.method == "POST":
        commentform = NoteCommentForm(request.POST,prefix="commentform")


        if commentform.is_valid():
            print "comment valid"
            note = open(path+".note",'r+')
            jload = json.loads(note.read())
            note.close()
            new = {}
            new['User'] = commentform.data["user"]
            new['Body'] = commentform.data["comment"]
            new['DateTime'] = int(time.time())

            comments=[]
            for com in jload['comment']:
                comment={}
                comment['user']=com['user']
                comment['body']=com['body']
                comment['datetime']=com['dateTime']
                comments.append(comment)

            comments.append(new)
            jload['comment']=comments

            output = json.dumps(jload)
            out = open(path+".note",'w+')
            out.write(output)
            out.close()

            return HttpResponseRedirect('/'+str(username)+'/'+str(project)+'/'+str(nname)+'/')
    else:
        print "both NOT valid"
        commentform = NoteCommentForm(prefix="commentform")

    noteForm = formset_factory(NoteForm,extra=0)
    formset = noteForm(initial=[{
        'content': str(info['note']['content']),
        'bg_colour' : str(info['note']['bg']),
        'tx_colour':str(info['note']['tx']),
        }],prefix="noteForm")

    body['note']=formset
    body['commentform']=commentform

    return render_to_response('view_note.html',body)

@csrf_protect
def edit_note(request, username, project, note):
    nname = note
    path = os.path.join(settings.REPO_ROOT,project,note)
    f = open(path+".note",'r')
    info = json.loads(f.read())
    f.close()
    body = {}
    if request.method == "POST":
        formset = NoteForm(request.POST,prefix="noteForm")

        if formset.is_valid():
            print "note valid"

            note = open(path+".note",'r+')

            jload = json.loads(note.read())
            note.close()
            jload['note']['content'] = formset.data['noteForm-0-content']
            jload['note']['bg'] = formset.data['noteForm-0-bg_colour']
            jload['note']['tx'] = formset.data['noteForm-0-tx_colour']

            print jload
            output = json.dumps(jload)
            out = open(path+".note",'w+')
            out.write(output)
            out.close()
    else:
        print "Error could not save"

    return HttpResponseRedirect('/'+str(username)+'/'+str(project)+'/'+str(nname)+'/')


@csrf_protect
@login_required(login_url='/login/')
def projectAddUser(request,pname):
    #this will add the person to the new project
    repo = Repository.objects.get(hashurl=pname)
    usera = User.objects.get(username=request.user.username)

    repo.user.add(usera)
    repo.save()
    return HttpResponseRedirect('/'+str(request.user.username)+'/')



