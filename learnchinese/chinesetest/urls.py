from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check', views.check, name='check'),
    path('reset', views.reset, name='reset'),
    path('shuffle', views.shuffle, name='shuffle'),
]
