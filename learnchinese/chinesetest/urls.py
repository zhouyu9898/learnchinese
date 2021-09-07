from django.urls import path

from . import views

app_name = 'chinesetest'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/<int:hsk>/', views.test, name='test'),
    path('check', views.check, name='check'),
    path('reset', views.reset, name='reset'),
]
