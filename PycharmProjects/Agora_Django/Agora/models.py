from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profiles(models.Model):
    """
    This table will hold the user info for the profiles.
    """
    user =  models.OneToOneField(User)
    blur = models.TextField()
    photo = models.ImageField(upload_to='%Y/%m/%d', blank=True, null=True)
    role = models.CharField(max_length=20)

class Notification(models.Model):
    """
    This Table will be to hold notification if they are needed
    """
    userto = models.ManyToManyField(User, related_name='to')
    userfrom = models.OneToOneField(User, related_name='from')
    body = models.TextField()
    datetofrom = models.DateTimeField()

class Repository(models.Model):
    """
    The Table will be:
    name of the repo
    public is if external user's can have access to it
    user is the people who can access the repo

    """
    name = models.CharField(max_length=100)
    loc = models.CharField(max_length=200)
    public = models.BooleanField()
    user =  models.ManyToManyField(User)
    hashurl = models.CharField(max_length=100)


    # user, blur, photo, , first name, last name, email