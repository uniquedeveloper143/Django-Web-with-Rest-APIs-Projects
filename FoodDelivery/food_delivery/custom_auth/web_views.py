from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from food_delivery.custom_auth.forms import UserRegister, UserLogin
import random

from food_delivery.custom_auth.models import ApplicationUser
from food_delivery.product.models import *

rand_code = random.randrange(100000, 999999)


def index(request):
    restaurant = list(Restaurant.objects.all())
    # print(restaurant)
    restaurant_rating = RestaurantRating.objects.all()
    # print(restaurant_rating.restaurant)
    # restaurant_ratings = RestaurantRating.objects.filter(restaurant__in=restaurant_rating.restaurant).aggregate(Avg('rating'))
    # print("aggregate", restaurant_ratings)
    # # for i in restaurant_rating:
    # #     restaurant_rating = RestaurantRating.objects.filter(restaurant=i.restaurant).aggregate(Avg('rating'))
    # #     print("aggregate", restaurant_rating)
    # print("restaurant_rating len", len(restaurant_ratings))

    cart_length = Cart.objects.filter(user_details=request.user)
    data = {
        "restaurant": restaurant,
        "restaurant_rating": restaurant_rating,
        "cart": len(cart_length)
    }
    return render(request, 'custom_auth/index.html', data)


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            data = {
                "email": email,
                "password": password,
                "name": name,
                "phone": phone
            }
            # print('pass', password)
            # form.save()
            # import pdb;
            # pdb.set_trace()
            # messages.success(request, 'Account created successfully')
            # data = UserLogin()
            # return redirect('login')
            print('OTP Code::', rand_code)
            # import pdb;pdb.set_trace()
            # verify.send(request.POST.get('phone'))
            return render(request, 'custom_auth/otp.html', data)

    else:
        form = UserRegister()
    return render(request, 'custom_auth/register.html', {"form": form})


def otp_verify(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    code = request.POST.get('OTP')
    error_message = None

    if (not code):
        error_message = "OTP fields are required!!"
    elif len(code) != 6:
        error_message = "OTP must be 6 digit !!"

    # elif rand_code != int(code):
    #     error_message = "OTP is not correct!!"

    logindata = UserLogin()

    data = {
        "email": email,
        "password": password,
        "name": name,
        "phone": phone,
        "error": error_message,
        "form": logindata
    }

    if error_message:
        return render(request, 'custom_auth/otp.html', data)

    # if verify.check(phone, code):
    if rand_code == int(code):
        # request.user.is_verified = True
        password = make_password(password)
        user = ApplicationUser(email=email, password=password, name=name, phone=phone)
        user.save()
        return redirect('web_auth:login')
    else:
        error_message = "OTP is not Verified!!"
        data["error"] = error_message
        return render(request, 'custom_auth/otp.html', data)


def forgot(request):
    return render(request, 'custom_auth/forgot.html')


def update_forgot(request):
    email = request.POST.get('email')
    user_email = ApplicationUser.objects.filter(email=email).first()
    user_phone = ApplicationUser.objects.filter(phone=email).first()

    error_message = None
    if not email:
        error_message = "Email is required!!"
    elif not user_email and not user_phone:
        error_message = "Email is not valid!! Please Enter correct Email"

    if not error_message:
        print("Code :: ", rand_code)
        return render(request, 'custom_auth/verify_otp_forgot_password.html', {"email": email})
    print(user_email)
    print(user_phone)
    return render(request, 'custom_auth/forgot.html', {"error": error_message})


def verify_otp_forgot_password(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_otp = request.POST.get('OTP')
    user_email = ApplicationUser.objects.filter(email=email).first()
    user_phone = ApplicationUser.objects.filter(phone=email).first()
    print(user_email)
    print(user_phone)
    print(password)
    error_message = None

    if (not user_otp):
        error_message = "OTP fields are required!!"
    elif len(user_otp) != 6:
        error_message = "OTP must be 6 digit !!"
    elif (not password):
        error_message = "Password is required!!"
    elif len(password) < 8:
        error_message = "Password must be 8 char or long!!"
    elif rand_code != int(user_otp):
        error_message = "OTP is not correct!!"

    if not error_message:
        password = make_password(password)
        if user_email:
            ApplicationUser.objects.filter(id=user_email.id).update(password=password)
        else:
            ApplicationUser.objects.filter(id=user_phone.id).update(password=password)
        return redirect('web_auth:login')

    else:
        return render(request, 'custom_auth/verify_otp_forgot_password.html', {"error": error_message, "email": email, "password": password, "otp": user_otp})


def logout(request):
    request.session.flush()
    return redirect('web_auth:login')


avg_rating = {}


def food_details(request):
    restaurant_id = request.GET.get('restaurant')
    food = Food.objects.filter(restaurant=restaurant_id)
    cart_length = Cart.objects.filter(user_details=request.user)
    favorite = Favorite.objects.all()

    data = {
        "food": food,
        "cart": len(cart_length),
        "favorite": favorite,
    }
    return render(request, 'custom_auth/food_details.html', data)


def selected_food(request):
    food_id = request.GET.get('food')
    print("food", food_id)
    food = Food.objects.filter(id=food_id)
    food_size = FoodSize.objects.filter(food=food_id)
    ingredient = Ingredient.objects.filter(food=food_id)
    rating_avg = FoodRating.objects.filter(food=food_id).aggregate(rating_avg=Avg("rating")).values()
    for rating in rating_avg:
        rating = rating

    cart_length = Cart.objects.filter(user_details=request.user)
    data = {
        "food": food,
        "ingredient": ingredient,
        "food_size": food_size,
        "rating_avg": rating,
        "cart": len(cart_length)
    }

    return render(request, 'custom_auth/selected_food.html', data)


def add_cart(request):
    if request.method == "POST":
        food_id = request.POST.get('food_id')
        food = Food.objects.get(id=food_id)
        quantity = request.POST.get('qty')
        food_size = int(request.POST.get('food_size'))
        print(food_size)
        # print(quantity)
        # print(request.user)
        cart = Cart(user_details=request.user, food_details=food, quantity=quantity, size=food_size)
        cart.save()
    return HttpResponse()


def like_food(request):
    if request.method == "POST":
        food_id = request.POST.get('food_id')
        food = Food.objects.get(id=food_id)
        favorite = Favorite.objects.filter(user_details=request.user, food_details=food).first()
        if favorite:
            if favorite.favorite_food == True:
                favorite.favorite_food = False
                favorite.save()
                # Favorite.objects.filter(id=food_id).update(favorite_food=False)
                # print("in ok")
            else:
                # Favorite.objects.filter(id=food_id).update(favorite_food=True)
                favorite.favorite_food = True
                favorite.save()
        else:
            favorite = Favorite.objects.get_or_create(user_details=request.user, food_details=food, favorite_food=True)
            favorite.save()
    return HttpResponse()


def cart_details(request):
    cart_length = Cart.objects.all()
    cart_length = Cart.objects.filter(user_details=request.user)
    # print(cart)
    # print("dhfggfhfsdh")
    return render(request, 'custom_auth/cart_details.html', {"cart_data": cart_length, "cart": len(cart_length)})


def order_place(request):
    cart = Cart.objects.filter(user_details=request.user)
    total_cart = len(cart)
    # print(total_cart)
    total = 0
    for cart_total in cart:
        total += cart_total.quantity * cart_total.food_details.price

    order = Order.objects.get_or_create(user=request.user, total_product=total_cart, total_amount=total)
    # order.save()
    # print("total", total)
    for carts in cart:
        # print(len(cart))
        order = Order.objects.get(user=request.user, total_product=total_cart, total_amount=total)
        food = Food.objects.get(pk=carts.food_details.id)
        food_name = carts.food_details.food_name
        price = float(carts.food_details.price)
        quantity = carts.quantity
        size = carts.size
        shipping_charge = carts.food_details.delivery_type
        sub_total = float(carts.quantity * carts.food_details.price)

        order_details = OrderDetails.objects.create(order=order, food=food, food_name=food_name, price=price, quantity=quantity, size=size, shipping_charge=shipping_charge, sub_total=sub_total)
        # order_details.save()
        carts.delete()
    return HttpResponse()

