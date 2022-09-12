from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Menu, TimeCoefficient, EmotionCoefficient, User, MenuReview, FoodTypeDetail


class MenuModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'food_type', 'food_type_detail', 'likes', 'dislikes', 'views', 'final_coefficient']
    list_display_links = ['title']
    list_filter = ['likes', 'dislikes']
    search_fields = ['title']
    list_editable = []

    class Meta:
        model = Menu


class FoodTypeDetailModelAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    search_fields = ['title']
    list_editable = []

    class Meta:
        model = FoodTypeDetail


class EmotionCoefficientModelAdmin(admin.ModelAdmin):
    list_display = ['menu_id', 'emotion', 'coefficient']
    list_display_links = ['menu_id']
    list_filter = ['emotion']
    search_fields = ['menu_id']
    list_editable = []

    class Meta:
        model = EmotionCoefficient


class TimeCoefficientModelAdmin(admin.ModelAdmin):
    list_display = ['menu_id', 'month', 'hour', 'coefficient']
    list_display_links = ['menu_id']
    list_filter = ['month', 'hour']
    search_fields = ['menu_id']
    list_editable = []

    class Meta:
        model = TimeCoefficient


class MenuReviewModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'menu_id', 'review']
    list_display_links = ['user_id']
    list_filter = ['user_id', 'menu_id']
    search_fields = ['user_id', 'menu_id']
    list_editable = []

    class Meta:
        model = TimeCoefficient


class UserModelAdmin(UserAdmin):
    list_display = ['university_id', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff']
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'university_id')}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'university_id')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    class Meta:
        model = User


admin.site.register(User, UserModelAdmin)
admin.site.register(Menu, MenuModelAdmin)
admin.site.register(FoodTypeDetail, FoodTypeDetailModelAdmin)
admin.site.register(TimeCoefficient, TimeCoefficientModelAdmin)
admin.site.register(EmotionCoefficient, EmotionCoefficientModelAdmin)
admin.site.register(MenuReview, MenuReviewModelAdmin)
