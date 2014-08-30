from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from Agora_Django import settings


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.contrib.auth.views.login',{'template_name' : 'login.html'}),
    # url(r'^blog/', include('blog.urls')),
    url(r'^system/admin/', include(admin.site.urls)),
    url(r'^app/register/$','Agora_android.views.appRegister'),
    url(r'^app/createproject/$','Agora_android.views.createProject'),
    url(r'^app/(?P<username>\w+)/$','Agora_android.views.appLogins'),
    url(r'^app/repo/(?P<pname>\w+)/note/(?P<nnote>\w+)/$','Agora_android.views.repoGetNote'),
    url(r'^app/repo/note/upload/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.repoUploadNote'),
    url(r'^app/repo/note/check/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.repoCheckNote'),
    url(r'^app/repo/(?P<pname>\w+)/(?P<uname>\w+)/add/$','Agora_android.views.addUserToRepo'),
    url(r'^app/repo/(?P<pname>\w+)/$','Agora_android.views.repoFileList'),
    url(r'^app/data/user/$','Agora_android.views.userRepoData'),
    url(r'^app/share/note/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.shareNote'),
    url(r'^app/share/project/(?P<pname>\w+)/$','Agora_android.views.shareProject'),
    url(r'^app/note/delete/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.deleteNote'),
    url(r'^add/user/(?P<pname>\w+)/$','Agora.views.projectAddUser'),
    url(r'login/', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^register/$','Agora.views.register'),
    url(r'^logout/$','Agora.views.logout_view'),
    url(r'^newuser/$','Agora.views.newuser'),
    url(r'home/$', 'Agora.views.home'),
    url(r'^error/(?P<mesg>\w+)','Agora.views.error'),
    url(r'^(?P<username>\w+)/$','Agora.views.profile',name='profile_view'),
    url(r'^(?P<username>\w+)/newproject/$','Agora.views.CreateRepoForUser'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/$','Agora.views.repoProject'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/createnote/$','Agora.views.new_note'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/(?P<note>\w+)/$','Agora.views.view_note'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/(?P<note>\w+)/editnote/$','Agora.views.edit_note'),


)
