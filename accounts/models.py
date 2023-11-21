from django.db import models
# inport user
from django.contrib.auth.models import AbstractUser as User , BaseUserManager
from django.contrib.auth.hashers import make_password
#modifying user model


class customUser(User):
    otp = models.CharField(max_length=4 ,null=True, blank=True)
    otp_valid_till = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def save(self, *args, **kwargs):
        self.password = make_password("password")
        print(self.password)
        if self.is_superuser == False:
            if "@msijanakpuri.com" not in self.email or len(self.email) == len("@msijanakpuri.com"):
                print(self.email)
                raise Exception("Email is not valid")
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs) 

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self.create_user(email, password, **extra_fields)


