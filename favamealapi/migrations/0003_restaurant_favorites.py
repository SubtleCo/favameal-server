# Generated by Django 3.1.3 on 2021-05-12 14:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favamealapi', '0002_auto_20201116_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='favorites',
            field=models.ManyToManyField(through='favamealapi.FavoriteRestaurant', to=settings.AUTH_USER_MODEL),
        ),
    ]
