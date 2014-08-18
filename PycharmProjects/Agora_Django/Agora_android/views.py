from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from Agora.models import Profiles
from Agora_git.functions import getFileRepo
from Agora_git.models import Repository


@csrf_exempt
def appLogins(request, username):
    logout(request)


    if request.method.decode('utf-8') == "POST":
        username = request.POST['username'].decode('utf-8')
        password = request.POST['password'].decode('utf-8')

        c = {}

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:

                login(request, user)

                responseProfile = Profiles.objects.get(user=User.objects.get(username=user).id)
                # responseData = serializers.serialize('json',Repository.objects.filter(user=User.objects.get(username=user).id))


                c['logged'] = "Welcome"
                c['first_name'] = responseProfile.user.first_name
                c['last_name'] = responseProfile.user.last_name
                c['email'] = responseProfile.user.email
                c['blur'] = responseProfile.blur
                c['photo'] = str(responseProfile.photo)
                c['cookie'] = request.session._session_key

                return HttpResponse(simplejson.dumps(c), content_type="application/json")

            else:


                c['logged'] = "Failed"

                return HttpResponse(simplejson.dumps(c), content_type="application/json")

        else:


            c['logged'] = "Failed"
            return HttpResponse(simplejson.dumps(c), content_type="application/json")


@csrf_exempt
def appRegister(request):

    if request.method.decode('utf-8') == "POST":

        print request.POST

        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']

        reply = {}

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # User Doesn't exist to create a new account
            print "Create a new User"
            reply['user'] = "created"
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname,
            )

            loginUser = authenticate(username=username, password=password)

            login(request, loginUser)

            reply['cookie'] = request.session._session_key

            return HttpResponse(json.dumps(reply), content_type="application/json")
        else:
            # user exists
            print "Username already taken"
            reply['user'] = "already"
            return HttpResponse(json.dumps(reply), content_type="application/json")


@csrf_exempt
def userRepoData(request):
    print request.POST
    reply = {}
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        print session_key

        user = userFromSession(session_key)
        print user
        if(user == 0):

            reply['reply'] = "error Session id"
            return HttpResponse(json.dumps(reply), content_type="application/json")
        else:

            repositories = Repository.objects.filter(user=user);
            list =[]
            reply['reply'] = "worked"
            list.append(reply)
            for rep in repositories:
                r = {}
                r['name'] = rep.name
                r['url'] = rep.hashurl
                list.append(r)

            print json.dumps(list)
            return HttpResponse(json.dumps(list), content_type="application/json")

    else:

        reply['reply'] = "error"
        return HttpResponse(json.dumps(reply), content_type="application/json")


def userFromSession(skey):
    try:
        ses = Session.objects.get(session_key=skey)
        userid = ses.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=userid)
    except Session.DoesNotExist:
        return 0
    except User.DoesNotExist:
        return 0
    else:
        return user


@csrf_exempt
def repoFileList(request,pname):

    reply = {}
    print request.POST
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        print session_key

        user = userFromSession(session_key)
        print user
        if(user == 0):

            reply['reply'] = "error Session id"
            return HttpResponse(json.dumps(reply), content_type="application/json")
        else:
            rname = Repository.objects.get(hashurl=pname).name
            if rname is not None:
                result = getFileRepo(rname)
                reply = []
                for rep in result:
                    l={}
                    l['name']=rep[0]
                    l['time']=rep[1]
                    reply.append(l)
                return HttpResponse(json.dumps(reply), content_type="application/json")

    else:
        reply['reply'] = "error Session id"
        return HttpResponse(json.dumps(reply), content_type="application/json")