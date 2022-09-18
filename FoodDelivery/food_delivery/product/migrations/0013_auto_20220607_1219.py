# Generated by Django 3.2 on 2022-06-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20220607_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sub_total',
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='sub_total',
            field=models.FloatField(default=0, null=True, verbose_name='Sub Total'),
        ),
    ]
