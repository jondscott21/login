from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^pokes$', views.pokes),
    url(r'^add_poke/(?P<id>\d+)$', views.add_poke),
    url(r'^log_in$', views.log_in),
    url(r'^log_out$', views.log_out),
    url(r'^.*$', views.error),

]
