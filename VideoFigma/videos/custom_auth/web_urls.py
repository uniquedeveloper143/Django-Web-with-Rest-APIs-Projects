from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib.auth import views as auth_views
from videos.custom_auth.web_views import index, register, send_sms, forgot, update_forgot, logout, verify_otp_forgot_password

app_name = 'web_auth'

urlpatterns = [

        # path('', home),
        path('index', index, name='index'),
        # path('', Index.as_view(), name="products"),
        path('register', register, name="register"), # this is function based views
        # path('register', Register.as_view(), name="register"),
        path('login/', auth_views.LoginView.as_view(template_name='custom_auth/login.html'), name='login'),
        path('send_sms', send_sms, name="send_sms"),
        path('verify_otp_forgot_password', verify_otp_forgot_password, name="verify_otp_forgot_password"),
        path('forgot', forgot, name="forgot"),
        path('update_forgot', update_forgot, name="update_forgot"),
        # path('login', Login.as_view(), name="login"),
        # path('update_pass', UpdatePass.as_view(), name="update_pass"),
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
