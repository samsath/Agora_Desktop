__author__ = 'sam'
import os

from django.conf import settings
from Agora.models import Repository
from django.contrib.auth.models import User
import time

def create_repo(rname,username):
    """
    This will create a repo in the directory with the project name then add it to the database
    :param name: ideal project name
    :return: either create or no
    """
    lname = username + "__" +  rname
    repo_dir = os.path.join(settings.REPO_ROOT, lname)
    if os.path.isdir(repo_dir):
        # The folder already exists
        return False
    else:
        os.makedirs(repo_dir)
        random = User.objects.make_random_password(100,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        hashcode = str(int(time.time()))+"_"+random

        repodb = Repository(
            name = rname,
            loc = lname,
            public = False,
            hashurl = hashcode,
        )
        repodb.save()
        return True

def user_repo(rname,uname):
    """
    This adds the user to a repostiory so they can access it.
    :param rname: repository name
    :param uname: user name
    :return: boolean if worked
    """
    pname = uname.username + "__" +  rname
    repo_dir = os.path.join(settings.REPO_ROOT, pname)
    try:
        repdb = Repository.objects.get(loc=pname)
    except Repository.DoesNotExist:
        return False
    else:
        try:
            usera = User.objects.get(username=uname)
        except User.DoesNotExist:
            return False
        else:

            #config = repo.config_writer()
            #config.set_value(
            #    uname.username,
            #    uname.first_name,
            #    uname.email
            #)

            if os.path.isdir(repo_dir) and repdb is not None:
                repdb.user.add(usera)
                repdb.save()
                return True
            else:
                return False

def getFileRepo(name):
    """
    path = os.path.join(settings.REPO_ROOT,project)
    result = []
    result += [ file for file in os.listdir(path) if file.endswith('.note')]
    :param name:
    :return:
    """
    print name
    result=[]
    repo_dir = os.path.join(settings.REPO_ROOT, name)
    if os.path.isdir(repo_dir):
        result += [ [file.title(),int(os.path.getmtime(repo_dir+"/"+file))] for file in os.listdir(repo_dir) if file.endswith('.note')]
    else:
        return None

    return result
