# Generated by Django 4.0.2 on 2022-05-17 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_alter_table_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='image',
            field=models.ImageField(max_length=300, upload_to='tables/', verbose_name='Картинка'),
        ),
    ]