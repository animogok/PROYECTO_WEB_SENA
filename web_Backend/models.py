from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher as By
from django.utils import timezone
from web_Backend.managers import CustomUserManager

# Create your models here.

class User_registrations(AbstractBaseUser ):

    firsName = models.CharField(blank = False)
    lastName = models.CharField( blank = False)
    idNumber = models.CharField(unique = True)
    email = models.EmailField(blank = False, unique = True)
    date_joined = models.DateTimeField(default = timezone.now)
    password = models.CharField(blank = False, unique = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fistName', 'lastName', 'password']
    
    objects = CustomUserManager
    
    def set_password(self, raw_password: str | None) -> None:
        return super().set_password(raw_password)
    
    def check_password(self, raw_password: str) -> bool:
        return super().check_password(raw_password)
    
    class Meta: 
        db_table = "users"
        db_table_comment = "User creation db table, for storing information"