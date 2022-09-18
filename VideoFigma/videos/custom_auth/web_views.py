from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .form import UserRegister, UserLogin
from .models import ApplicationUser
from ..post.models import Category, Post, Favourite, UserPhoto
import random
from . import verify


def index(request):
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Post.get_all_products_by_category_id(categoryID)
    else:
        products = Post.get_all_products()

    data = {}
    data['favourite'] = Favourite.objects.all()
    data['popular'] = Post.objects.filter(popular=True)
    data['products'] = products
    data['categories'] = categories
    # user = UserPhoto.objects.filter(user=request.user).first()
    # if not user:
    #     user = ''
    data['new_release'] = Post.objects.all().order_by("-created")[:4]

    return render(request, 'custom_auth/index.html', data)


code = random.randrange(1000, 9999)


def forgot(request):
    return render(request, 'custom_auth/forgot.html')


def verify_otp_forgot_password(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_otp = request.POST.get('OTP')
    userData = ApplicationUser.objects.filter(email=email).first()
    print(userData)
    print(password)
    error_message = None

    if (not user_otp):
        error_message = "OTP fields are required!!"
    elif len(user_otp) != 4:
        error_message = "OTP must be 4 digit !!"
    elif (not password):
        error_message = "Password is required!!"
    elif len(password) < 8:
        error_message = "Password must be 8 char or long!!"
    elif code != int(user_otp):
        error_message = "OTP is not correct!!"

    if not error_message:
        password = make_password(password)
        ApplicationUser.objects.filter(id=userData.id).update(password=password)
        return render(request, 'custom_auth/login.html')

    else:
        return render(request, 'custom_auth/verify_otp_forgot_password.html', {"error": error_message, "email": email, "password": password, "otp": user_otp})


def update_forgot(request):
    email = request.POST.get('email')
    userData = ApplicationUser.objects.filter(email=email).first()

    error_message = None
    if (not email):
        error_message = "Email is required!!"
    elif (not userData):
        error_message = "Email is not valid!! Please Enter correct Email"

    # elif (not password):
    #     error_message = "Password is required!!"
    # elif len(password) < 8:
    #     error_message = "Password must be 8 char or long!!"
    # print(userData.id)
    if not error_message:
        # password = make_password(password)
        # ApplicationUser.objects.filter(id=userData.id).update(password=password)
        print("Code :: ", code)
        return render(request, 'custom_auth/verify_otp_forgot_password.html', {"email": email})
    print(userData)
    return render(request, 'custom_auth/forgot.html', {"error": error_message})


def send_sms(request):
    email = request.POST.get('email')
    email1 = request.POST.get('email1')
    password = request.POST.get('password')
    print('email', email)
    print('email1', email1)
    print('pass', password)
    otp = request.POST.get('OTP')
    error_message = None

    if (not email):
        error_message = "Email fields are required!!"
    elif (not otp):
        error_message = "OTP fields are required!!"
    elif len(otp) != 4:
        error_message = "OTP must be 4 digit !!"

    if error_message:
        return render(request, 'custom_auth/otp.html', {"error": error_message, "email": email1, "password": password})

    # code = form.cleaned_data.get('code')
    # if verify.check(request.user.phone, code):
    #     request.user.is_verified = True
    elif code == int(otp):
        password = make_password(password)
        user = ApplicationUser(email=email, password=password)
        user.save()
        return render(request, 'custom_auth/login.html')
    else:
        error_message = "OTP is not correct!!"
        return render(request, 'custom_auth/otp.html', {"code": code, "email": email, "error": error_message, "password": password})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # data = {
            #     "email": email,
            #     "password": password
            # }
            # print('pass', password)
            # form.save()
            # import pdb;
            # pdb.set_trace()
            # messages.success(request, 'Account created successfully')
            # data = UserLogin()
            # return redirect('login')
            print('code::', code)
            verify.send(form.cleaned_data.get('phone'))
            return render(request, 'custom_auth/otp.html', {"email": email, "password": password})

    else:
        form = UserRegister()
    return render(request, 'custom_auth/register.html', {"form": form})


def logout(request):
    # request.session.clear()
    request.session.flush()
    return redirect('web_auth:index')

# class Login(View):
#     # return_url = None
#     def get(self, request):
#         # Login.return_url = request.GET.get('return_url')
#         return render(request, 'custom_auth/login.html')
#
#     def post(self, request):
#         if request.method == 'GET':
#             return render(request, 'custom_auth/login.html')
#         else:
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             customer = ApplicationUser.objects.filter(email=email)
#             print(customer)
#             error_message = None
#             if customer:
#                 # val = check_password(password, customer.password)
#                 val = customer.set_password(customer.password)
#                 print('ballll',val)
#                 if val:
#                     request.session['customer'] = customer.id
#                     return redirect('index')
#                     # if Login.return_url:
#                     #     return HttpResponseRedirect(Login.return_url)
#                     # else:
#                     #     Login.return_url = None
#                     #     return redirect('products')
#                 else:
#                     error_message = 'Email or Password is invalid!!'
#
#             else:
#                 error_message = 'Email or Password is invalid!!'
#             return render(request, 'custom_auth/login.html', {'error': error_message})


# def login(request):
#     print('gjkfdslgkds;lds')
#     if request.method == 'POST':
#         form = UserAuthSerializer(data=request.POST)
#         # form = UserLogin()
#         print('gdegsdfhfdhfgs111112')
#         print(form)
#         if form.is_valid():
#             print('gdegsdfhfdhfgs11111')
#             # email = form.cleaned_data.get('email')
#             # password = form.cleaned_data.get('password')
#             # print(email)
#             user = authenticate(request, **form.data)
#             print('user == ', user)
#             if not user:
#                 messages.warning(request, f'Invalid User')
#                 form = UserLogin()
#                 return render(request, 'custom_auth/login.html', {"form": form})
#             else:
#                 return render(request, 'custom_auth/index.html', {"form": form})
#
#         # user_details = BaseUserSerializer(instance=user, context={'request': request, 'view': self}).data
#         #
#         # user_details.update(self.get_success_headers(user))
#
#         # return Response(data=user_details, status=status.HTTP_200_OK)
#     else:
#         UserLogin()
#     return render(request, 'custom_auth/login.html')
