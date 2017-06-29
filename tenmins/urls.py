"""tenmins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from website.views import listing, index_login, index_register, detail, detail_vote
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout

from website.mobile_views import video_list
from website.api import video, video_card
from rest_framework.authtoken import views

#---------------------------------作业代码（开始）-------------------------------
from website.mobile_views import user_list_panel_login, user_list_panel, user_detail

from website.api import userlist, userlist_operation, userdetail

#---------------------------------作业代码（结束）-------------------------------

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^list/$', listing, name='list'),
    url(r'^list/(?P<cate>[A-Za-z]+)$', listing, name='list'),
    url(r'^detail/(?P<id>\d+)$', detail, name='detail'),
    url(r'^detail/vote/(?P<id>\d+)$', detail_vote, name='vote'),
    url(r'^login/$', index_login, name='login'),
    url(r'^register/$', index_register, name='register'),
    url(r'^logout/$', logout, {'next_page': '/register'}, name='logout'),



    url(r'^api/videos/$', video),
    url(r'^api/videos/(?P<id>\d+)$', video_card),
    url(r'^api/token-auth$', views.obtain_auth_token),

    url(r'^m/videolist/', video_list),

#---------------------------------作业代码（开始）-------------------------------
    #开始：mobile_views 的 url
    url(r'^m/userlistpanel/login/$', user_list_panel_login, name="user_list_panel_login"),
    #注：别忘了 from django.contrib.auth.views import logout
    #note: difference between "/..." and "..."
        # is the former redirects to localhost/8000/...
        # and the latter redirects to current_url/...
    url(r'^m/userlistpanel/logout/$', logout, {'next_page': '/m/userlistpanel/login'}),
    url(r'^m/userlistpanel/$', user_list_panel, name="user_list_panel"),
    url(r'^m/userdetail/(?P<id>\d+)$', user_detail),

    #结束：mobile_views 的 url

    #开始：api 的 url
    url(r'^api/userlist/$', userlist),
    url(r'^api/userlist/(?P<id>\d+)$', userlist_operation),
    url(r'^api/userdetail/(?P<id>\d+)$', userdetail),
    # url(r'^api/token-auth$', views.obtain_auth_token),

    #结束：api 的 url

#---------------------------------作业代码（结束）-------------------------------

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
