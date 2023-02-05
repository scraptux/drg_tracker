from django.urls import include, path
from rest_framework import routers
from .views import YearsViewSet, KapitelViewSet, GruppenViewSet, KodesViewSet, track, search

router = routers.DefaultRouter()
router.register(r'version', YearsViewSet)
router.register(r'kapitel', KapitelViewSet)
router.register(r'gruppe', GruppenViewSet)
router.register(r'kode', KodesViewSet)

urlpatterns = [
    path('track/', track),
    path('search/', search)
]

urlpatterns += router.urls