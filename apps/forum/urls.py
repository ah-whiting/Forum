from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^topics/new$', views.new_topic),
    url(r'^topics$', views.create_topic),
    url(r'^topics/(?P<id>\d+)$', views.show_topic),
    # url(r'^topics/(?P<id>\d+)/edit$', views.edit_topic),
    # url(r'^topics/(?P<id>\d+)/update$', views.update_topic),
    url(r'^topics/(?P<id>\d+)/delete$', views.delete_topic),
    url(r'^topics/(?P<id>\d+)/comments$', views.create_comment),
    url(r'^comments/(?P<id>\d+)$', views.update_comment),
    url(r'^comments/(?P<id>\d+)/delete$', views.delete_comment),
]