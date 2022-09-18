from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from food_delivery.custom_auth.utils import get_restaurant_photo_path, get_food_photo_path


class Restaurant(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=150, unique=True, blank=True, null=True,
                            error_messages={'unique': _('A category with that name already exists.')})
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    delivery_type = models.CharField(null=True, blank=True, default="Free", max_length=100)
    delivery_time = models.TimeField(null=True, blank=True)
    avg_rating = models.FloatField(blank=True, null=True,)
    food_image = models.FileField(
        upload_to=get_restaurant_photo_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class RestaurantRating(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurant_rating_user")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_rating_details")
    rating = models.FloatField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        verbose_name = _('RestaurantRating')
        verbose_name_plural = _('RestaurantRatings')

    def __str__(self):
        return f'{self.restaurant}'


class Food(TimeStampedModel):

    # DELIVERY_TYPES = Choices(
    #     ("free", "Free"),
    #     ("female", "Female"),
    # )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_details')
    food_name = models.CharField(
                                 verbose_name=_('Food Name'),
                                 max_length=150,
                                 blank=True,
                                 null=True,
                                 help_text=_('Food Name'))
    delivery_type = models.CharField(null=True, blank=True, default="Free", max_length=100)
    delivery_time = models.TimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True,)
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    avg_rating = models.FloatField(blank=True, null=True,)
    food_image = models.FileField(
        upload_to=get_food_photo_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')

    def __str__(self):
        return f'{self.food_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.food_name)
        super().save(*args, **kwargs)


class FoodRating(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_rating_user")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="food_rating_details")
    rating = models.FloatField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        verbose_name = _('FoodRating')
        verbose_name_plural = _('FoodRatings')

    def __str__(self):
        return f'{self.food}'


class FoodSize(TimeStampedModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food_size_details')
    size = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('FoodSize')
        verbose_name_plural = _('FoodSizes')

    def __str__(self):
        return f'{self.food}'


class Ingredient(TimeStampedModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='ingredient_food_details')
    name = models.CharField(_('Ingredient Name'), max_length=150,  blank=True, null=True,)

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        return f'{self.name}'


class Cart(TimeStampedModel):
    user_details = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_cart_user")
    food_details = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="food_cart_details")
    quantity = models.IntegerField(_('Quantity'), blank=True, null=True, validators=[MinValueValidator(1)], default=1)
    size = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'{self.quantity}'


class Favorite(TimeStampedModel):
    user_details = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_favorite_user")
    food_details = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="food_favorite_details")
    favorite_food = models.BooleanField(_('Favorite Food'), blank=True, null=True)

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return f'{self.favorite_food}'


class Order(TimeStampedModel):
    PAYMENT_TYPE = Choices(
        ("cod", "Cash On Delivery"),
        ("upi", "UPI"),
        ("card", "Card"),
    )

    ORDER_STATUS = Choices(
        ("pending", "Pending"),
        ("canceled", "Canceled"),
        ("returned", "Returned"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("on_the_way", "On The Way"),
        ("dispatch", "Dispatch"),
        ("shipped", "Sipped"),
        ("delivered", "Delivered"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    total_product = models.IntegerField(_('Total Product'), default=0, null=True)
    address = models.CharField(_('Address'), max_length=255,  blank=True, null=True, default="Ahmedabad")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default=PAYMENT_TYPE.cod)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default=ORDER_STATUS.pending)
    total_amount = models.FloatField(_('Total Amount'), default=0, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user}'


class OrderDetails(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    food_name = models.CharField(
                                 verbose_name=_('Food Name'),
                                 max_length=150,
                                 blank=True,
                                 null=True,
                                 help_text=_('Food Name'))
    price = models.FloatField(_('Food Price'), null=True, blank=True)
    quantity = models.FloatField(_('Quantity'), null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    shipping_charge = models.CharField(_('Shipping Charge'), default=0, null=True, max_length=100,)
    sub_total = models.FloatField(_('Sub Total'), default=0, null=True)

    class Meta:
        verbose_name = _('OrderDetail')
        verbose_name_plural = _('OrderDetails')

    def __str__(self):
        return f'{self.order}'
