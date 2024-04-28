from .models import User_registrations
from django import forms

class FormularioRegistrodeUsuarios(forms.ModelForm):
    class Meta:
        model = User_registrations
        fields = [
            'firsName', 'lastName', 'idNumber', 'email', 'birth_date', 'password'
        ]