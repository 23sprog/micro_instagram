# Generated by Django 4.1.2 on 2023-01-07 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='سن'),
        ),
    ]