from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profiles(models.Model):
    user =  models.OneToOneField(User)
    blur = models.TextField()
    photo = models.ImageField(upload_to='%Y/%m/%d', blank=True, null=True)
    role = models.CharField(max_length=20)

class Notification(models.Model):
    userto = models.ManyToManyField(User, related_name='to')
    userfrom = models.OneToOneField(User, related_name='from')
    body = models.TextField()
    datetofrom = models.DateTimeField()

    # user, blur, photo, , first name, last name, email