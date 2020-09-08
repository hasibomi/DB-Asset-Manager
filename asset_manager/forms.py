from django import forms
from .models import Connection


class NewConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'
