"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path
from apps.post.views import IndexView, post_detail, PostsListView, search, PostCreateView, PostUpdateView, PostDeleteView
from apps.accounts.views import login_view, signup_view, logout_view, UserUpdateView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',IndexView.as_view(), name='home'),
    url(r'^blog/$', PostsListView.as_view(), name='blog'),
    path('create/',PostCreateView.as_view(), name='post_create'),
    path('blog/<slug>/',post_detail, name='post_detail'),
    path('blog/<slug>/update',PostUpdateView.as_view(), name='post_update'),
    path('blog/<slug>/delete',PostDeleteView.as_view(), name='post_delete'),
    path('search/',search, name='search'),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup_view, name='signup'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^myaccount/$', UserUpdateView.as_view(), name='my_account'),
    # path(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)