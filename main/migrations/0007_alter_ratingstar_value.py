# Generated by Django 3.2.6 on 2021-08-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_liked_ads_likes_liked_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingstar',
            name='value',
            field=models.IntegerField(default=0, verbose_name='value'),
        ),
    ]