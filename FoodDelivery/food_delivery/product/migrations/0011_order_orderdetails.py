# Generated by Django 3.2 on 2022-06-07 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0010_cart_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('food_name', models.CharField(blank=True, help_text='Food Name', max_length=150, null=True, verbose_name='Food Name')),
                ('price', models.FloatField(verbose_name='Food Price')),
                ('quantity', models.FloatField(verbose_name='Quantity')),
                ('size', models.IntegerField(blank=True, null=True)),
                ('shipping_charge', models.FloatField(default=0, null=True, verbose_name='Shipping Charge')),
                ('address', models.CharField(blank=True, default='Ahmedabad', max_length=255, null=True, verbose_name='Address')),
                ('payment_type', models.CharField(choices=[('cod', 'Cash On Delivery'), ('upi', 'UPI'), ('card', 'Card')], default='cod', max_length=10)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('canceled', 'Canceled'), ('returned', 'Returned'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('on_the_way', 'On The Way'), ('dispatch', 'Dispatch'), ('shipped', 'Sipped'), ('delivered', 'Delivered')], default='pending', max_length=10)),
                ('sub_total', models.FloatField(default=0, null=True, verbose_name='Sub Total')),
                ('food', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('total_product', models.IntegerField(default=0, null=True, verbose_name='Total Product')),
                ('total_amount', models.FloatField(default=0, null=True, verbose_name='Total Amount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='product.order')),
            ],
            options={
                'verbose_name': 'OrderDetail',
                'verbose_name_plural': 'OrderDetails',
            },
        ),
    ]