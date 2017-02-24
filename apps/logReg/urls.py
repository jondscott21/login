from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^travels$', views.travels),
    # needs regex for id
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^add$', views.add),
    url(r'^proc_add$', views.proc_add),
    url(r'^log_in$', views.log_in),
    url(r'^log_out$', views.log_out),
    url(r'^.*$', views.error),

]
