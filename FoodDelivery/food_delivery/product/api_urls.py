from django.urls import path, include
from rest_framework import routers
from food_delivery.product import views

router = routers.SimpleRouter()

router.register('restaurant', views.RestaurantViewSet, basename='restaurant')
router.register('restaurant_rating', views.RestaurantRatingViewSet, basename='restaurant_rating')
router.register('food', views.FoodViewSet, basename='food')
router.register('food_size', views.FoodSizeViewSet, basename='food_size')
router.register('food_rating', views.FoodRatingViewSet, basename='food_rating')
router.register('ingredient', views.IngredientViewSet, basename='ingredient')
router.register('favorite_food', views.FavoriteViewSet, basename='favorite_food')
router.register('cart', views.CartViewSet, basename='cart')

app_name = 'product'

urlpatterns = [

        path('', include(router.urls)),
]

