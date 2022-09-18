from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .form import UserRegister, UserLogin
import random
from .models import ApplicationUser
from ..post.models import Category, SubCategory, Post, Comment, CommentReply, Like, DisLike
from . import verify
rand_code = random.randrange(100000, 999999)


def index(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    sub_category_id = request.GET.get('sub_category')
    # print("sub_category_id", sub_category_id)
    sub_category = SubCategory.objects.filter(category=category_id)
    post = Post.objects.filter(sub_category=sub_category_id)
    # sub_category_name = post.sub_category.sub_category_name
    # print(sub_category_name)
    data = {
        "categories": categories,
        "sub_category": sub_category,
        "post": post,

    }
    return render(request, 'custom_auth/index.html', data)


def post_details(request):
    post_id = request.GET.get('post')
    print("post", post_id)
    post = Post.objects.filter(id=post_id)
    category_id = Post.objects.filter(id=post_id).first()

    category_id = category_id.sub_category.category.id
    comment = Comment.objects.filter(post=post_id)
    likes = Like.objects.filter(like_count=True)
    dislikes = Like.objects.filter(like_count=False)
    print("category_id", category_id)
    return render(request, 'custom_auth/post_details.html', {"post": post, "category_id": category_id, "comment": comment, "total_comments": len(comment), "likes": likes})


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

    if verify.check(phone, code):
    # if rand_code == int(code):
        # request.user.is_verified = True
        password = make_password(password)
        user = ApplicationUser(email=email, password=password, name=name, phone=phone)
        user.save()
        return redirect('web_auth:login')
    else:
        error_message = "OTP is not Verified!!"
        data["error"] = error_message
        return render(request, 'custom_auth/otp.html', data)


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
            verify.send(request.POST.get('phone'))
            return render(request, 'custom_auth/otp.html', data)

    else:
        form = UserRegister()
    return render(request, 'custom_auth/register.html', {"form": form})


def logout(request):
    request.session.flush()
    return render(request, 'custom_auth/login.html')


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
    elif rand_code != int(user_otp):
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

    if not error_message:
        print("Code :: ", rand_code)
        return render(request, 'custom_auth/verify_otp_forgot_password.html', {"email": email})
    print(userData)
    return render(request, 'custom_auth/forgot.html', {"error": error_message})


def set_comment(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        message = request.POST.get('message')
        user_id = int(request.POST.get('user'))
        # print("post_id", post_id)
        # print("message", message)
        # print("user", user_id)
        comment = Comment(post=post, message=message, user=request.user)
        comment.save()
    return HttpResponse()


def reply_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        rep_message = request.POST.get('rep_message')

        user_id = int(request.POST.get('user'))
        print("comment_id", comment_id)
        print("message", comment)
        print("user", user_id)
        comment = CommentReply(comment=comment, message=rep_message, user=request.user)
        comment.save()
    return HttpResponse()


def like_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        user_id = int(request.POST.get('user'))
        flag = request.POST.get('flag')
        print("flag", flag)
        print("comment_id", comment_id)
        print("comment", comment)
        print("user", user_id)
        print("post", post)

        if flag == "0":
            dislike = DisLike.objects.filter(comment=comment, post=post, dislike_count=True, user=request.user)
            dislike.delete()

            like = Like.objects.get_or_create(comment=comment, post=post, like_count=True, user=request.user)
            like.save()
        else:
            like = Like.objects.filter(comment=comment, post=post, like_count=True, user=request.user)
            like.delete()

            dislike = DisLike.objects.get_or_create(comment=comment, post=post, dislike_count=True, user=request.user)
            dislike.save()

    return HttpResponse()
