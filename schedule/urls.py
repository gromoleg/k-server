from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^faculties$', views.faculties, name='faculties'),
    url(r'^groups$', views.groups, name='groups'),
]