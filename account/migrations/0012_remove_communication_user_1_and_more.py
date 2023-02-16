# Generated by Django 4.1.2 on 2023-01-10 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0011_remove_direct_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communication',
            name='user_1',
        ),
        migrations.RemoveField(
            model_name='communication',
            name='user_2',
        ),
        migrations.AddField(
            model_name='communication',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='communication',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='communication',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, verbose_name='کاربران'),
        ),
    ]