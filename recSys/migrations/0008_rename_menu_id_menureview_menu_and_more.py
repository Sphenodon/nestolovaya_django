# Generated by Django 4.0.2 on 2022-03-26 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recSys', '0007_menureview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menureview',
            old_name='menu_id',
            new_name='menu',
        ),
        migrations.RenameField(
            model_name='menureview',
            old_name='user_id',
            new_name='user',
        ),
    ]
