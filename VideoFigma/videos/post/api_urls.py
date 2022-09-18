from django.urls import path, include
from rest_framework import routers
from videos.post import views

router = routers.SimpleRouter()

router.register('post', views.PostViewSet, basename='post')
router.register('category', views.CategoryViewSet, basename='category')
router.register('favorite', views.FavouriteViewSet, basename='favorite')
# router.register('popular', views.popular, basename='popular')

app_name = 'post'

urlpatterns = [

        path('', include(router.urls)),
        # path('popular/', views.popular),
]

