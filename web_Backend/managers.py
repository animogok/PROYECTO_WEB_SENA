from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise(ValueError)
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using =self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise(ValueError)
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Super User must have staff"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Super user booleand field Error"))
        return self.create_user(email, password, **extra_fields)