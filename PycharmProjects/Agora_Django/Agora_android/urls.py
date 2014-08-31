from django.conf.urls import url

urlpatterns = [
    url(r'^register/$','Agora_android.views.appRegister'),
    url(r'^createproject/$','Agora_android.views.createProject'),
    url(r'^(?P<username>\w+)/$','Agora_android.views.appLogins'),
    url(r'^repo/(?P<pname>\w+)/note/(?P<nnote>\w+)/$','Agora_android.views.repoGetNote'),
    url(r'^repo/note/upload/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.repoUploadNote'),
    url(r'^repo/note/check/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.repoCheckNote'),
    url(r'^repo/(?P<pname>\w+)/(?P<uname>\w+)/add/$','Agora_android.views.addUserToRepo'),
    url(r'^repo/(?P<pname>\w+)/$','Agora_android.views.repoFileList'),
    url(r'^data/user/$','Agora_android.views.userRepoData'),
    url(r'^share/note/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.shareNote'),
    url(r'^share/project/(?P<pname>\w+)/$','Agora_android.views.shareProject'),
    url(r'^note/delete/(?P<pname>\w+)/(?P<nnote>\w+)/$','Agora_android.views.deleteNote'),
]