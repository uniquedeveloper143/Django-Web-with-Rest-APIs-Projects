from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from food_delivery.product.models import RestaurantRating, FoodRating


@receiver(post_save, sender=RestaurantRating)
def restaurant_avg_rating(sender, instance, **kwargs):
    if instance is not None:
        restaurant = instance.restaurant
        rating = RestaurantRating.objects.filter(restaurant=restaurant).aggregate(rating=Avg('rating'))
        print("rating : ", rating.get('rating'))

        restaurant.avg_rating = rating.get('rating')
        print("restaurant.avg_rating :", restaurant.avg_rating)
        restaurant.save()


@receiver(post_save, sender=FoodRating)
def food_avg_rating(sender, instance, **kwargs):
    if instance is not None:
        food = instance.food
        rating = FoodRating.objects.filter(food=food).aggregate(rating=Avg('rating'))
        print("rating : ", rating.get('rating'))

        food.avg_rating = rating.get('rating')
        print("food.avg_rating :", food.avg_rating)
        food.save()

