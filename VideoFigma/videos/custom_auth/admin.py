from datetime import timedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Case, When, Value
from django.utils import timezone
from videos.custom_auth.models import ApplicationUser


admin.site.unregister(Group)
admin.site.site_header = 'Figma Videos Admin Panel'
admin.site.site_title = 'Videos playlist'
admin.site.index_title = 'Admin Panel'


@admin.register(ApplicationUser)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        ('Personal info', {'fields': ('uuid', 'username', 'name', 'email', 'password')}),
        ('Statuses', {'fields': ('is_active', 'is_email_verified',)}),
        ('Service', {'fields': ('is_staff', 'is_superuser',)}),
        ('Accounts dates', {'fields': ('last_login', 'last_user_activity', 'last_modified',)}),
    )

    readonly_fields = ('uuid', 'username', 'name', 'last_modified',)
    list_display = ('username', 'name', 'email', '_get_password', 'uuid', 'last_user_activity', 'is_online')
    search_fields = ('username', 'email', 'uuid', 'name')
    list_filter = ('username', 'email', 'uuid', 'name')

    def _get_password(self, obj):
        return 'Yes' if obj.password not in [None, ''] else 'No'

    _get_password.short_description = 'PASSWORD'
    _get_password.admin_order_field = 'password'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            is_online=Case(
                When(last_user_activity__gte=timezone.now() - timedelta(minutes=5), then=Value(True)),
                default=Value(False)

            )
        )

    def is_online(self, obj):
        return obj.is_online

    is_online.boolean = True
    is_online.admin_order_field = 'is_online'



