# Generated by Django 4.0.2 on 2022-05-15 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recSys', '0015_foodtype_alter_emotioncoefficient_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FoodType',
            new_name='FoodTypeDetail',
        ),
        migrations.AlterField(
            model_name='emotioncoefficient',
            name='coefficient',
            field=models.IntegerField(default=0, verbose_name='Коэффициент по эмоции'),
        ),
        migrations.AlterField(
            model_name='timecoefficient',
            name='coefficient',
            field=models.IntegerField(default=0, verbose_name='Коэффициент по времени'),
        ),
    ]