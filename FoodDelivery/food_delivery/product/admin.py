from django.contrib import admin

from food_delivery.product.models import *


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('restaurant', 'food_name', 'slug', 'delivery_type', 'delivery_time', 'description', 'food_image', 'avg_rating', 'price', 'created', 'modified')
    search_fields = ('restaurant', 'food_name', 'slug', 'delivery_type', 'delivery_time',)
    list_filter = ('restaurant', 'food_name', 'slug', 'delivery_type', 'delivery_time',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('user', 'name', 'food_image', 'avg_rating', 'slug', 'created', 'modified')
    search_fields = ('name', 'slug', 'avg_rating')
    list_filter = ('name', 'slug',)


@admin.register(FoodSize)
class FoodSizeAdmin(admin.ModelAdmin):
    list_display = ('food', 'size',)
    search_fields = ('food', 'size',)
    list_filter = ('food', 'size',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('food', 'name',)
    search_fields = ('food', 'name',)
    list_filter = ('food', 'name',)


@admin.register(FoodRating)
class FoodRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'rating',)
    search_fields = ('food', 'rating',)
    list_filter = ('food', 'rating',)


@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating',)
    search_fields = ('restaurant', 'rating',)
    list_filter = ('restaurant', 'rating',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'food_details', 'favorite_food',)
    search_fields = ('food_details', 'favorite_food',)
    list_filter = ('food_details', 'favorite_food',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'food_details', 'quantity', 'size')
    search_fields = ('food_details', 'quantity',)
    list_filter = ('food_details', 'quantity',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_product', 'total_amount')
    # search_fields = ('food_details', 'quantity',)
    # list_filter = ('food_details', 'quantity',)


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'food_name', 'size')
    # search_fields = ('food_details', 'quantity',)
    # list_filter = ('food_details', 'quantity',)
