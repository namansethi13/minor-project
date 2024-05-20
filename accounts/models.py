from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import uuid
from django.core.mail import send_mail
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password=uuid.uuid4().hex[:8]
        user.set_password(password)
        if self.is_staff:
            subject="Resultly:Admin Account Created Sucessfully" 
            message=f"Your admin account has been created sucessfully. Your username is {self.email} and password is {password}. Use forget password to reset your password."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.email]
            send_mail(subject,message,email_from,recipient_list)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class customUser(AbstractUser):
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_valid_till = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            if "@msijanakpuri.com" not in self.email or len(self.email) == len("@msijanakpuri.com"):
                raise Exception("Email is not valid")
        
                
            

        super().save(*args, **kwargs)
        


