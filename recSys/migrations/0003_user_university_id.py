# Generated by Django 4.0.2 on 2022-03-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recSys', '0002_alter_menureview_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='university_id',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='University_id'),
        ),
    ]