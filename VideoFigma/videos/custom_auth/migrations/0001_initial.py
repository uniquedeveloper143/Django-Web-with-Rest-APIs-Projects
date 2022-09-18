# Generated by Django 3.2 on 2022-05-20 05:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import uuid
import videos.custom_auth.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(default=uuid.uuid4, error_messages={'unique': 'A user with that uuid already exists.'}, help_text='Required. A 32 hexadecimal digits number as specified in RFC 4122.', unique=True, verbose_name='uuid')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. A 32 hexadecimal digits number as specified in RFC 4122.', max_length=150, null=True, unique=True, verbose_name='username')),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'A user with that email already exists.'}, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('is_email_verified', models.BooleanField(default=True, verbose_name='email verified')),
                ('name', models.CharField(blank=True, help_text='Full name ', max_length=150, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect theis instead of deleting accounts.', verbose_name='active')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('last_user_activity', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last activity')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', videos.custom_auth.managers.ApplicationUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetId',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('expire_time', models.DateTimeField(default=datetime.datetime(2022, 5, 21, 5, 42, 8, 279437, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PasswordResetId',
            },
        ),
    ]
