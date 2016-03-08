"""social_blog URL Configuration

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
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from blog_app.views import Home, SignUpView, UserListView, BlogCreateView, BlogListView, \
    MyPostsView, MyFollowingListView, follow_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='home_view'),
    url(r'^login/', auth_views.login, name='login_view'),
    url(r'^logout/', auth_views.logout_then_login, name='logout_view'),
    url(r'^sign_up/', SignUpView.as_view(), name='sign_up_view'),
    url(r'^users/$', UserListView.as_view(), name='user_list_view'),
    url(r'^new_post/$', login_required(BlogCreateView.as_view()), name='new_post'),
    url(r'^my_posts/$', login_required(MyPostsView.as_view()), name='my_posts'),
    url(r'^user/(?P<pk>\d+)/posts/$', login_required(BlogListView.as_view()), name='user_post_list'),
    url(r'^follow/(?P<user_id>\d+)$', follow_user, name='follow_user'),
    url(r'^my_following/$', login_required(MyFollowingListView.as_view()), name='my_following_view')
]
