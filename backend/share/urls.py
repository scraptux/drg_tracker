from django.urls import include, path
from rest_framework import routers
from .views import sharedata

router = routers.DefaultRouter()

urlpatterns = [
    path('code/', sharedata)
]

urlpatterns += router.urls