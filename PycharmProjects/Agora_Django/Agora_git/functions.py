__author__ = 'sam'
import os
from git import *
from django.conf import settings
from models import Repository
from django.contrib.auth.models import User



def get_completelist():
    """
    This goes through the main repo fodler and displays all the projects.
    :return: list of the Agora_git repo's on the server
    """
    repos = [get_repo(direct) for direct in os.listdir(settings.REPOS_ROOT)]
    return [rep for rep in repos if not (rep is None)]

def get_repo(name):
    """
    This returns Agora_git header of a repository
    :param name: the name of the repo from the Agora_git dir
    :return: Agora_git active header for that project
    """
    repo_dir = os.path.join(settings.REPO_ROOT, name)
    if os.path.isdir(repo_dir):
        try:
            print Repo(repo_dir)
            return Repo(repo_dir)
        except Exception:
            pass
    return None

def get_commit(name,commit):
    """
    This returns the commit header from the one suggested
    :param name: repo name
    :param commit: commit name
    :return:commit object
    """
    repo = get_repo(name)
    comit = repo.commit(commit)
    return comit

def get_blob(name, commit, file):
    """
    This returns the blob information of a project
    :param name: project name
    :param commit: commit header
    :param file:
    :return:
    """
    repo = get_repo(name)
    commit = repo.commit(commit)
    tree = commit.tree

    for path in file.split(os.sep):
        t = tree.get(path)
        if isinstance(t, Tree):
            tree = t
        else:
            blob = t
    return blob

def create_repo(rname):
    """
    This will create a repo in the directory with the project name then add it to the database
    :param name: ideal project name
    :return: either create or no
    """
    repo_dir = os.path.join(settings.REPO_ROOT, rname)
    if os.path.isdir(repo_dir):
        # The folder already exists
        return False
    else:
        os.makedirs(repo_dir)
        repo = Repo.init(repo_dir,bare=False)
        assert repo.bare == False
        repo.config_writer()

        repodb = Repository(
            name = rname,
            public = False
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
    repo_dir = os.path.join(settings.REPO_ROOT, rname)
    try:
        repdb = Repository.objects.get(name=rname)
    except Repository.DoesNotExist:
        return False
    else:
        # add user to the repo information
        repo = get_repo(rname)
        try:
            usera = User.objects.get(username=uname)
        except User.DoesNotExist:
            return False
        else:

            config = repo.config_writer()
            config.set_value(
                uname.username,
                uname.first_name,
                uname.email
            )

            if os.path.isdir(repo_dir) and repdb is not None:
                repdb.user.add(usera)
                repdb.save()
                return True
            else:
                return False

def add_file(rname,file):
    """
    Adds a new file to the repo
    :param rname:  repository name
    :param file: file location
    :return: prints the new_commit so you can see if it works
    """

    repo = get_repo(rname)
    index = repo.index
    index.add([file])
    new_commit = index.commit("")

    return True

def remove_file(rname,file):
    """
    Remove file form the repo
    :param rname: repository name
    :param file: file location
    :return: prints the new_commit so you can see if it works
    """
    repo = get_repo(rname)
    index = repo.index()
    index.remove([file])
    new_commit = index.commit("removed")
    return new_commit