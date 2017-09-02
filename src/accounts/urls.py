from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from .views import (
	UserDetailView,
	UserFollowView,
	login_view, 
	register_view, 
	logout_view,
)


urlpatterns = [
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),

]