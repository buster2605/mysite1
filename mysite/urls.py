from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views
from polls.forms import LoginForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
)
