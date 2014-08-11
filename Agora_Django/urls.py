from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.contrib.auth.views.login',{'template_name' : 'login.html'}),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^register/$','Agora.views.register'),
    url(r'^logout/$','Agora.views.logout_view'),
    url(r'^newuser/$','Agora.views.newuser'),
    url(r'^home/$', 'Agora.views.home'),



)
