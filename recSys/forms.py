from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from recSys.models import User, Menu, FoodTypeDetail


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'university_id')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'university_id')


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('title', 'composition', 'food_type', 'food_type_detail', 'image', 'price', 'weight', 'available')


class FoodTypeDetailForm(forms.ModelForm):

    class Meta:
        model = FoodTypeDetail
        fields = ('title',)
