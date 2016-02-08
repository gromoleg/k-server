from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^faculties$', views.faculties, name='faculties'),
    url(r'^groups$', views.groups, name='groups'),
    url(r'^(?P<group_id>[0-9]+)$', views.group, name='group'),
    url(r'^(?P<group_id>[0-9]+)/(?P<class_id>[0-9]+)$', views.group_class, name='group_class'),
]