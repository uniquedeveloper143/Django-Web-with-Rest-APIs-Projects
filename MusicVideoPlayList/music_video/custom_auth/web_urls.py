from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib.auth import views as auth_views
from music_video.custom_auth.web_views import index, register, otp_verify, logout, verify_otp_forgot_password, forgot, update_forgot ,post_details, set_comment, reply_comment , like_comment

app_name = 'web_auth'

urlpatterns = [

        path('index', index, name='index'),
        path('register', register, name="register"), # this is function based views
        path('', auth_views.LoginView.as_view(template_name='custom_auth/login.html'), name='login'),
        path('otp_verify', otp_verify, name="otp_verify"),
        path('verify_otp_forgot_password', verify_otp_forgot_password, name="verify_otp_forgot_password"),
        path('forgot', forgot, name="forgot"),
        path('update_forgot', update_forgot, name="update_forgot"),
        path('post_details', post_details, name="post_details"),
        path('set_comment', set_comment, name="set_comment"),
        path('reply_comment', reply_comment, name="reply_comment"),
        path('like_comment', like_comment, name="like_comment"),
        # # path('update_pass', UpdatePass.as_view(), name="update_pass"),
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
