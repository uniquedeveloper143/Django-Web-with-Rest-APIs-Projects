# Generated by Django 3.2 on 2022-05-21 07:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_alter_passwordresetid_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='passwordresetid',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 22, 7, 11, 46, 443760, tzinfo=utc)),
        ),
    ]
