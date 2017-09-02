from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import (
    PostListAPIView,
    LikeToggleAPIView
    )

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='postlist'), # /api/tweet/
    url(r'^(?P<slug>[\w-]+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),
]

