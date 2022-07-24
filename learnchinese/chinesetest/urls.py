from django.urls import path

from . import views

app_name = 'chinesetest'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/<int:hsk>/', views.test, name='test'),
    path('check', views.check, name='check'),
    path('reset/<int:hsk>/', views.reset, name='reset'),
    path('random/<int:hsk>/', views.random, name='random'),
]
