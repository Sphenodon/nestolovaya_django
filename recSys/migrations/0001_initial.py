# Generated by Django 4.0.2 on 2022-03-21 20:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('composition', models.TextField(max_length=2047, verbose_name='Состав')),
                ('weight', models.CharField(default=0, max_length=100, verbose_name='Вес')),
                ('price', models.SmallIntegerField(default=0, verbose_name='Цена')),
                ('food_type', models.CharField(choices=[('FO', 'food'), ('DR', 'drinks'), ('DE', 'dessert'), ('CO', 'combo')], help_text='Тип еды', max_length=2, verbose_name='Тип еды')),
                ('image', models.CharField(default='/resources/static/img/menu-coffee.jpg', max_length=300, verbose_name='Ссылка на картинку')),
                ('likes', models.IntegerField(default=0, verbose_name='Лайки')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Дизлайки')),
                ('views', models.BigIntegerField(default=0, verbose_name='Просмотры')),
                ('final_coefficient', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=300)], verbose_name='Итоговый коэффициент')),
            ],
            options={
                'verbose_name': 'Еда',
                'verbose_name_plural': 'Еда',
                'db_table': 'menu',
            },
        ),
        migrations.CreateModel(
            name='TimeCoefficient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.SmallIntegerField(verbose_name='Месяц, в который работает коэффициент')),
                ('hour', models.SmallIntegerField(verbose_name='Час, в который работает коэффициент')),
                ('coefficient', models.FloatField(default=50, validators=[django.core.validators.MaxValueValidator(limit_value=100)], verbose_name='Коэффициент по времени')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recSys.menu', verbose_name='Блюдо, напиток и т.д. из меню')),
            ],
            options={
                'verbose_name': 'Коэффициент по времени',
                'verbose_name_plural': 'Коэффициенты по времени',
                'db_table': 'time_coefficient',
            },
        ),
        migrations.CreateModel(
            name='MenuReview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.BooleanField(null=True, verbose_name='like or dislike')),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recSys.menu', verbose_name='menu_id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user id')),
            ],
            options={
                'verbose_name': 'Лайк или дизлайк',
                'verbose_name_plural': 'Лайк или дизлайк',
                'db_table': 'menu_review',
            },
        ),
        migrations.CreateModel(
            name='EmotionCoefficient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emotion', models.CharField(choices=[('HA', 'happy'), ('NE', 'neutral'), ('SA', 'sad'), ('AN', 'angry')], max_length=2, verbose_name='Эмоция')),
                ('coefficient', models.FloatField(default=50, validators=[django.core.validators.MaxValueValidator(limit_value=100)], verbose_name='Коэффициент по эмоции')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recSys.menu', verbose_name='Блюдо, напиток и т.д. из меню')),
            ],
            options={
                'verbose_name': 'Коэффициент по эмоции',
                'verbose_name_plural': 'Коэффициенты по эмоции',
                'db_table': 'emotion_coefficient',
            },
        ),
    ]