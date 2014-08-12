from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Repository(models.Model):
    """
    The Table will be:
    name of the repo
    public is if external user's can have access to it
    user is the people who can access the repo

    """
    name = models.CharField(max_length=100)
    public = models.BooleanField()
    user =  models.ManyToManyField(User)
