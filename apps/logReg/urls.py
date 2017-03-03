from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^quotes$', views.quotes),
    url(r'^addquote$', views.addquote),
    url(r'^add_fav/(?P<id>\d+)$', views.add_fav),
    url(r'^rem_fav/(?P<id>\d+)$', views.rem_fav),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^log_in$', views.log_in),
    url(r'^log_out$', views.log_out),
    url(r'^.*$', views.error),
]
