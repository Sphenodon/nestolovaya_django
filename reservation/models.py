from datetime import date
from django.utils import timezone

from nestolovaya_itmo.s3_storage import CustomStorage
from recSys.models import User
from django.db import models


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(max_length=300, upload_to='tables/', storage=CustomStorage, verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        db_table = 'table'


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_creation = models.DateField(default=date.today, verbose_name='Дата создания бронирования')
    date_of_reservation = models.DateField(default=date.today, verbose_name='Дата бронирования')
    time_of_reservation = models.TimeField(default=timezone.now, verbose_name='Время бронирования')
    user = models.ForeignKey('recSys.User', null=False, on_delete=models.CASCADE)
    table = models.ForeignKey('Table', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return 'table: %s, user: %s %s, time: %s' % (self.table.title, self.user.first_name, self.user.last_name, self.date_of_reservation)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        db_table = 'reservation'
