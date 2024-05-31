from rest_framework import serializers
from .models import User_registrations

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User_registrations
        fields = ['email','firsName', 'lastName', 'idNumber','password', 'is_staff']