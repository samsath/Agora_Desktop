from django.conf.urls import patterns, include, url


from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.contrib.auth.views.login',{'template_name' : 'login.html'}),
    # url(r'^blog/', include('blog.urls')),

    url(r'^system/admin/', include(admin.site.urls)),
    url(r'^app/register/$','Agora_android.views.appRegister'),
    url(r'^app/(?P<username>\w+)/$','Agora_android.views.appLogins'),
    url(r'^app/data/user/$','Agora_android.views.userRepoData'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^register/$','Agora.views.register'),
    url(r'^logout/$','Agora.views.logout_view'),
    url(r'^newuser/$','Agora.views.newuser'),
    url(r'^home/$', 'Agora.views.home'),
    url(r'^error/(?P<mesg>\w+)','Agora.views.error'),
    url(r'^(?P<username>\w+)/$','Agora.views.profile',name='profile_view'),
    url(r'^(?P<username>\w+)/newproject/$','Agora.views.CreateRepoForUser'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/$','Agora.views.repoProject'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/createnote/$','Agora.views.new_note'),
    url(r'^(?P<username>\w+)/(?P<project>\w+)/(?P<note>\w+)/$','Agora.views.view_note'),

)
