from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone_number, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        if not phone_number:
            raise ValueError('Phone number must be provided')
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        if not phone_number:
            raise ValueError('Phone number must be provided')
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=155)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email', ]

    objects = MyUserManager()

    def __str__(self):
        return f'{self.username} - {self.phone_number}'

    def create_activation_code(self):
        import hashlib

        code = self.email + str(self.id)
        encoded = code.encode()
        md5_object = hashlib.md5(encoded)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

