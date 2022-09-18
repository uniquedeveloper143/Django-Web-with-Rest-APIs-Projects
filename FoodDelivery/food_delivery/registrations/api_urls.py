from django.urls import path, include
from rest_framework import routers
from food_delivery.registrations import views

router = routers.SimpleRouter()

router.register('', views.RegistrationViewSet, basename='registration')

app_name = 'registrations'

urlpatterns = [

        path('', include(router.urls)),
]

