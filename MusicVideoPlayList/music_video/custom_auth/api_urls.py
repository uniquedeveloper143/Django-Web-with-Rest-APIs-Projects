from django.urls import path, include
from rest_framework import routers
from music_video.custom_auth import views

router = routers.SimpleRouter()

router.register('auth', views.UserAuthViewSet, basename='auth')

app_name = 'custom_auth'

urlpatterns = [

        path('', include(router.urls)),
]

