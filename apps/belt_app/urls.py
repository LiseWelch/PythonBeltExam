from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.root),
    url(r'^success$', views.success),
    url(r'^process$', views.process),
    url(r'^logout$', views.logout),
    url(r'^appointments/add$', views.add_new),
    url(r'^appointments$', views.all_appts),
    url(r'^create$', views.create),
    url(r'^appointments/(?P<id>([1-9]+[0-9]*))$', views.edit),
    url(r'^delete/(?P<id>([1-9]+[0-9]*))$', views.delete),
    url(r'^update/(?P<id>([1-9]+[0-9]*))$', views.update),
    url(r'^.*/$', views.catch)

]