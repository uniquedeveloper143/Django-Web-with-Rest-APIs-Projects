from django.urls import path, include
from rest_framework import routers
from music_video.post import views

router = routers.SimpleRouter()

router.register('category', views.CategoryViewSet, basename='category')
router.register('sub_category', views.SubCategoryViewSet, basename='sub_category')
router.register('post', views.PostViewSet, basename='post')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('reply', views.CommentReplyViewSet, basename='reply')

app_name = 'post'

urlpatterns = [

        path('', include(router.urls)),
]

