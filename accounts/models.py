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