from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('version/', views.version),
    path('kapitel/', views.kapitel),
    path('gruppe/', views.gruppen),
    path('kode/', views.kodes),
    path('track/', views.track),
    path('search/', views.search)
]