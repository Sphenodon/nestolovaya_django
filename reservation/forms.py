from django import forms

from reservation.models import Table


class TableCreationForm(forms.ModelForm):

    class Meta:
        model = Table
        fields = '__all__'


class TableChangeForm(forms.ModelForm):

    class Meta:
        model = Table
        fields = '__all__'
