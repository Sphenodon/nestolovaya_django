# Generated by Django 4.0.2 on 2022-03-31 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recSys', '0009_alter_user_university_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Продается в данный момент'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(max_length=300, upload_to='images/menu/', verbose_name='Картинка'),
        ),
    ]