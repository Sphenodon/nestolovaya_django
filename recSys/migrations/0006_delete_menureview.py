# Generated by Django 4.0.2 on 2022-03-26 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recSys', '0005_remove_menureview_like_or_dislike'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MenuReview',
        ),
    ]