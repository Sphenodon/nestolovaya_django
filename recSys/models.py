from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

from nestolovaya_itmo.s3_storage import CustomStorage


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Название')
    composition = models.TextField(max_length=2047, verbose_name='Состав')
    weight = models.CharField(default=0, max_length=100, verbose_name='Вес')
    price = models.SmallIntegerField(default=0, verbose_name='Цена')

    FOOD_TYPE = (
        ('FO', 'Блюда'),
        ('DR', 'Напитки'),
        ('DE', 'Десерты'),
        ('CO', 'Комбо')
    )

    food_type = models.CharField(max_length=2, choices=FOOD_TYPE, help_text='Тип еды', verbose_name='Тип еды')
    food_type_detail = models.ForeignKey('FoodTypeDetail', null=True, on_delete=models.SET_NULL, verbose_name='Тип еды подробнее')
    image = models.ImageField(max_length=300, upload_to='menu/', storage=CustomStorage, verbose_name='Картинка')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')
    views = models.BigIntegerField(default=0, verbose_name='Просмотры')
    final_coefficient = models.SmallIntegerField(default=0, verbose_name='Итоговый коэффициент')
    available = models.BooleanField(default=True, verbose_name='Продается в данный момент')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        db_table = 'menu'


class FoodTypeDetail(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, verbose_name='Тип еды подробнее')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип еды подробнее'
        verbose_name_plural = 'Тип еды подробнее'
        db_table = 'food_type'


class TimeCoefficient(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey('Menu', null=True, on_delete=models.CASCADE, verbose_name='Блюдо, напиток и т.д. из меню')
    month = models.SmallIntegerField(verbose_name='Месяц, в который работает коэффициент')
    hour = models.SmallIntegerField(verbose_name='Час, в который работает коэффициент')
    coefficient = models.IntegerField(default=0, verbose_name='Коэффициент по времени')

    def __str__(self):
        return '%s, month: %s, hour: %s, coefficient: %s' % (self.menu.title, self.month, self.hour, self.coefficient)

    class Meta:
        verbose_name = 'Коэффициент время'
        verbose_name_plural = 'Коэффициенты время'
        db_table = 'time_coefficient'


class EmotionCoefficient(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey('Menu', null=True, on_delete=models.CASCADE, verbose_name='Блюдо, напиток и т.д. из меню')

    EMOTION_TYPE = (
        ('HA', 'happy'),
        ('NE', 'neutral'),
        ('SA', 'sad'),
        ('AN', 'angry')
    )

    emotion = models.CharField(max_length=2, choices=EMOTION_TYPE, verbose_name='Эмоция')
    coefficient = models.IntegerField(default=0, verbose_name='Коэффициент по эмоции')

    def __str__(self):
        return '%s, emotion: %s, coefficient: %s' % (self.menu.title, self.emotion, self.coefficient)

    class Meta:
        verbose_name = 'Коэффициент настроения'
        verbose_name_plural = 'Коэффициенты настроения'
        db_table = 'emotion_coefficient'


class MenuReview(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', null=False, on_delete=models.CASCADE, verbose_name='user id')
    menu = models.ForeignKey('Menu', null=False, on_delete=models.CASCADE, verbose_name='menu_id')
    review = models.BooleanField(null=True, verbose_name='like или dislike')

    def __str__(self):
        return 'user_id: %s, menu_id: %s, review: %s' % (self.user_id, self.menu_id, self.review)

    class Meta:
        verbose_name = 'Лайк или дизлайк'
        verbose_name_plural = 'Лайк или дизлайк'
        db_table = 'menu_review'


class User(AbstractUser):
    university_id = models.PositiveIntegerField(default=000000, verbose_name='University_id')

    def __str__(self):
        return self.username

