from typing import Any
from django.core.exceptions import ValidationError
from .models import User_registrations
from django import forms


class FormularioRegistrodeUsuarios(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User_registrations
        fields = [
            'firsName', 'lastName', 'idNumber', 'email'
        ]
    
    #we generate something similar to the override in java language, where we acces to save() method of the father class, and then we hash directly the password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    
class FormularioLogin(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput)


class FormChangeData(forms.Form):
    email = forms.EmailInput()
    email_confirmation = forms.EmailInput()
        
        
    
       