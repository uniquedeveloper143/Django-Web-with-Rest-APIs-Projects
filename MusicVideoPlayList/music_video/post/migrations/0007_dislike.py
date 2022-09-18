# Generated by Django 3.2 on 2022-05-31 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0006_rename_likes_like_like_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dislike_count', models.BooleanField(blank=True, null=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_dislike', to='post.comment')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='post_dislike', to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_dislike', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DisLike',
                'verbose_name_plural': 'DisLikes',
            },
        ),
    ]
