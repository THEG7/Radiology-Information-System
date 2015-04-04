from django.conf.urls import patterns, include, url
from django.contrib import admin
import main.views as views
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RIS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ris/$', views.HomePageView.as_view(), name='home'),
    url(r'^ris/register/$', views.register, name='register'),
    url(r'^ris/login/$', views.user_login, name='login'),
    url(r'^ris/logout/$', views.user_logout, name='logout'),
    # url(r'^ris/record/create/$', views.UpdateRecordWizardView.as_view(views.FORMS), name='create_record'),
    url(r'^ris/record/create/$', views.create_radiology_record, name='create_record'),
    url(r'^ris/record/search/$', views.SearchRecordsView.as_view(), name='search_records'),
    url(r'^ris/record/(?P<record_id>\d+)/update/$', views.UpdateRadiologyRecordView.as_view(), name='update_record'),
    url(r'^ris/record/(?P<record_id>\d+)/images/$', views.ThumbnailImageView.as_view(), name='thumbnails'),
    url(r'^ris/images/add/$', views.AddImageView.as_view(), name='add_image'),
    url(r'^ris/images/(?P<image_id>\d+)/regular/$', views.RegularImageView.as_view(), name='regular_image'),
    url(r'^ris/images/(?P<image_id>\d+)/full/$', views.FullImageView.as_view(), name='full_image'),
    url(r'^ris/olap/$', staff_member_required(views.DataCubeView.as_view()), name='olap'),

)
