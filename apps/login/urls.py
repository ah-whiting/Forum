from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.root),
    url(r'^register$', views.create_user),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout)
]