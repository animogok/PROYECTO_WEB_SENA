from typing import Any
from .models import User_registrations
from django import forms
from django.forms import PasswordInput


class FormularioRegistrodeUsuarios(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User_registrations
        fields = [
            'firsName', 'lastName', 'idNumber', 'email'
        ]
        # Generar los ajustes necesarios los dias siguientes Sebastian, se organiza el widget para que la contraseña ingresada sea oculta a la hora de escribir
    
    def save(self, commit=True):
       
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    

    
    
    
       