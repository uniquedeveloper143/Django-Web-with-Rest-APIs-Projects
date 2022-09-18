from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib.auth import views as auth_views
from food_delivery.custom_auth.web_views import *

app_name = 'web_auth'

urlpatterns = [

        path('index', index, name='index'),
        path('register', register, name="register"), # this is function based views
        path('', auth_views.LoginView.as_view(template_name='custom_auth/login.html'), name='login'),
        path('otp_verify', otp_verify, name="otp_verify"),
        path('verify_otp_forgot_password', verify_otp_forgot_password, name="verify_otp_forgot_password"),
        path('forgot', forgot, name="forgot"),
        path('update_forgot', update_forgot, name="update_forgot"),
        path('food_details', food_details, name="food_details"),
        path('selected_food', selected_food, name="selected_food"),
        path('add_cart', add_cart, name="add_cart"),
        path('cart_details', cart_details, name="cart_details"),
        path('like_food', like_food, name="like_food"),
        path('order_place', order_place, name="order_place"),
        # # # path('update_pass', UpdatePass.as_view(), name="update_pass"),
        path('logout', logout, name="logout"),

        #
        # path('view_address', view_add, name="view_address"),
        # path('delete(<int:eid>)', delete_add, name='delete'),
        # path('edit_add(<int:eid>)', edit_add, name='edit_add'),
        # path('edit_data_add/<int:eid>', edit_data_add, name='edit_data_add'),
        # path('change_password', change_password, name="change_password"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
