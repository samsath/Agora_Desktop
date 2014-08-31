from django.conf.urls import patterns, include, url
from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from Agora_Django import settings


admin.autodiscover()

urlpatterns = [
    url(r'^$', 'django.contrib.auth.views.login',{'template_name' : 'login.html'}),
    url(r'^system/admin/', include(admin.site.urls),name='adminsite'),
    url(r'^app/',include('Agora_android.urls')),
    url(r'^add/user/(?P<pname>\w+)/$','Agora.views.projectAddUser',name='addUser'),
    url(r'login/', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^register/$','Agora.views.register',name='register'),
    url(r'^logout/$','Agora.views.logout_view',name='logout'),
    url(r'^newuser/$','Agora.views.newuser',name='newuser'),
    url(r'home/$', 'Agora.views.home', name='home'),
    url(r'^error/(?P<mesg>\w+)','Agora.views.error', name='error'),
    url(r'^(?P<username>\w+)/$','Agora.views.profile', name='profile_view'),
    url(r'^(?P<username>\w+)/newproject/$','Agora.views.CreateRepoForUser',name='createRepo'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/$','Agora.views.repoProject',name='projects'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/createnote/$','Agora.views.new_note',name='createnote'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/(?P<note>\w+)/$','Agora.views.view_note',name='viewnote'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/(?P<note>\w+)/editnote/$','Agora.views.edit_note',name='editnote'),
    ]
