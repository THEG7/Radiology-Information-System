from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import HomePageView, register, user_login, user_logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RIS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^ris/$', HomePageView.as_view(), name='home'),
    url(r'^ris/register/$', register, name='register'),
    url(r'^ris/login/$', user_login, name='login'),
    url(r'^ris/logout/$', user_logout, name='logout'),
)
