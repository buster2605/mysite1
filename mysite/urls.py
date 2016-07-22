from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views
from polls.forms import LoginForm
from polls.views import register_page #, base_page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', base_page, name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', views.login),
    url(r'^register/$', register_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
)
