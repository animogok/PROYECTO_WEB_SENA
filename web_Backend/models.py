from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.utils import timezone
from web_Backend.managers import CustomUserManager

# Create your models here.


# Templates used for DB creations models for the project
class User_registrations(AbstractBaseUser):

    firsName = models.CharField(blank = False)
    lastName = models.CharField( blank = False)
    idNumber = models.CharField(unique = True)
    email = models.EmailField(blank = False, unique = True)
    date_joined = models.DateTimeField(default = timezone.now)
    is_staff = models.BooleanField(default = False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['firsName', 'lastName', 'password']

    objects = CustomUserManager()
    
    class Meta: 
        db_table = "users"
        db_table_comment = "User creation db table, for storing information"
   

'''
This part from here will be used for validations inside de db, also, this will work like a middleware
''' 

