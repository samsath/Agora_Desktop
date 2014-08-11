__author__ = 'sam'
from git import *
from django.conf import settings
from models import Repository


def get_completelist():
    """
    This goes through the main repo fodler and displays all the projects.
    :return: list of the git repo's on the server
    """
    repos = [get_repo(direct) for direct in os.listdir(settings.REPOS_ROOT)]
    return [rep for rep in repos if not (rep is None)]

def get_repo(name):
    """
    This returns git header of a repository
    :param name: the name of the repo from the git dir
    :return: git active header for that project
    """
    repo_dir = os.path.join(settings.REPOS_ROOT, name)
    if os.path.isdir(repo_dir):
        try:
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

def create_repo(name):
    """
    This will create a repo in the directory with the project name then add it to the database
    :param name: ideal project name
    :return: either create or no
    """
    repo_dir = os.path.join(settings.REPOS_ROOT, name)
    if os.path.isdir(repo_dir):
        # The folder already exists
        return False
    else:
        os.makedirs(repo_dir)
        repo = Repo(repo_dir, bare=True)
        assert repo.bare == True
        repodb = Repository(name=name,public=False,user='')
        repodb.save()
        return True

def userrepo(rname,uname):
    """
    This adds the user to a repostiory so they can access it.
    :param rname: repository name
    :param uname: user name
    :return: boolean if worked
    """
    repo_dir = os.path.join(settings.REPOS_ROOT, rname)
    try:
        repdb = Repository.objects.get(name=rname)
    except Repository.DoesNotExist:
        return False
    else:
        if os.path.isdir(repo_dir) and repdb is not None:
            repdb.user = uname
            repdb.save()
            return True
        else:
            return False
