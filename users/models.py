from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from hashids import Hashids

class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, middle_name='', password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        user.generate_hashed_id()
        return user

    def create_superuser(self, phone_number, first_name, last_name, middle_name='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('date_joined', timezone.now())

        return self.create_user(phone_number, first_name, last_name, middle_name, password, **extra_fields)

class User(AbstractUser):
    username = None  # Удаляем поле username
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    iin = models.CharField(max_length=12, null=True, blank=True, verbose_name="ИИН")
    hashed_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'iin']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed_id:
            self.generate_hashed_id()

    def generate_hashed_id(self):
        hashids = Hashids(salt="your_secret_salt")
        self.hashed_id = hashids.encode(self.id)
        self.save()
