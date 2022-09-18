# Generated by Django 3.2 on 2022-05-26 11:07

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A user with that phone already exists.'}, max_length=128, null=True, region=None, unique=True, verbose_name='phone'),
        ),
    ]