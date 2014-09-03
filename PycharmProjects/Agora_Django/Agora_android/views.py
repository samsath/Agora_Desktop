from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
import json
from Agora.models import Profiles
from Agora_Django import settings
from Agora import function
from Agora.function import getFileRepo
from Agora.models import Repository
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import os


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
        if (user == 0):

            reply['reply'] = "error Session id"
            return HttpResponse(json.dumps(reply), content_type="application/json")
        else:

            repositories = Repository.objects.filter(user=user);
            list = []
            reply['reply'] = "worked"
            list.append(reply)
            for rep in repositories:
                r = {'name': rep.name, 'url': rep.hashurl}
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
def repoFileList(request, pname):
    reply = {}
    print request.POST
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        print session_key

        user = userFromSession(session_key)
        print user
        if (user == 0):

            reply['reply'] = "error Session id"
            return HttpResponse(json.dumps(reply), content_type="application/json")
        else:
            rname = Repository.objects.get(hashurl=pname).loc
            if rname is not None:
                result = getFileRepo(rname)
                reply = []
                for rep in result:
                    l = {'name': rep[0].lower(), 'time': rep[1]}
                    reply.append(l)

                print reply
                return HttpResponse(json.dumps(reply), content_type="application/json")

    else:
        reply['reply'] = "error Session id"
        return HttpResponse(json.dumps(reply), content_type="application/json")


def repoGetNote(requst, pname,nnote ):
    rname = Repository.objects.get(hashurl=pname).loc
    path = os.path.join(settings.REPO_ROOT, rname, nnote)
    f = open(path + ".note", 'r')
    info = json.loads(f.read())
    print info
    return HttpResponse(json.dumps(info), content_type="application/json")


def repoUploadNote(request, pname, nnote):
    print "New Note to save to server"
    print request.POST
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        print session_key
        rname = Repository.objects.get(hashurl=pname).loc
        user = userFromSession(session_key)
        print user
        if (user != 0):
            filename = nnote + ".note"
            content = json.loads(request.POST['file'])
            print content
            output = open(os.path.join(settings.REPO_ROOT, rname, filename.lower()), 'w')
            output.write(json.dumps(content))
            output.close()


def repoCheckNote(request, pname, nnote):
    print "Update of NOTE +========"
    print request.POST
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        print session_key
        rname = Repository.objects.get(hashurl=pname).loc
        print rname
        user = userFromSession(session_key)
        print user
        if user != 0:
            path = os.path.join(settings.REPO_ROOT, rname, nnote)
            if path.endswith(".note"):
                filename = path
            else:
                filename = path + ".note"
            print filename
            content = request.POST['file']
            print content
            snote = open(filename, 'r')
            print snote
            fromDevice = json.loads(content)
            fromServer = json.loads(snote.read())
            snote.close()

            if fromDevice == fromServer:
                # the files are the same
                return HttpResponse(json.dumps(fromDevice), content_type="application/json")

            else:
                # The files are different so now compare them.
                new = {}
                if int(fromDevice['note']['datetime']) > int(fromServer['note']['datetime']):
                    # the device is newer than server
                    new['note'] = fromDevice['note']

                else:
                    # server is newer than device
                    new['note'] = fromServer['note']

                complist = fromDevice['comment'] + fromServer['comment']
                result = [dict(compare) for compare in set(tuple(item.items()) for item in complist)]
                new['comment'] = result

                archivelist = fromDevice['archive'] + fromServer['archive']
                result = [dict(compare) for compare in set(tuple(item.items()) for item in archivelist)]
                new['archive'] = result

                # once everything has been compared it returns the new file.
                print new
                print json.dumps(new)
                snote = open(filename, 'w+')
                snote.write(json.dumps(new))
                snote.close()
                return HttpResponse(json.dumps(new), content_type="application/json")


def addUserToRepo(request, pname, uname):
    # # TODO finish this but so that it adds a user to the repo.
    return None


def shareNote(request, pname, nnote):
    # As you can only have project not notes on their own
    # TODO possible add just a url forward here to the note
    shareProject(request, pname)


def shareProject(request, pname):
    # This is to send out a share project request to any person on the list
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        email = request.POST['email']
        rname = Repository.objects.get(hashurl=pname).name
        link = settings.DOMAIN + "/add/user/" + pname

        subject = "Project Invite"
        from_email = settings.EMAIL_HOST_USER
        to = email

        htmly = get_template('email.html')
        plain = str(htmly)

        fill = Context({'project': rname.replace("_", " "), 'link': link})
        text_content = plain.render(fill)
        html_content = htmly.render(fill)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def deleteNote(request, pname, nnote):
    # this is to delete the sellected note. Instead of deleting the file it is just renamed to a .delete so it is clear
    filename = nnote + ".note"
    rname = Repository.objects.get(hashurl=pname).loc
    path = os.path.join(settings.REPO_ROOT, rname)
    result = []
    result += [file for file in os.listdir(path) if file.endswith('.note')]
    if filename in result:
        os.rename(filename, filename.replace(".note", ".delete"))


def createProject(request):
    if request.method.decode('utf-8') == "POST":
        session_key = request.POST['session_key']
        pname = request.POST['project']
        print "project name = " + pname
        user = userFromSession(session_key)
        if (user != 0):
            function.create_repo(pname,user.username)
            function.user_repo(pname, user)
