from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is a required field')
        """creates new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class Hero(models.Model):
    """Hero model"""
    alias = models.CharField(max_length=255, unique=True)
    alter_ego = models.CharField(max_length=255, unique=True)


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model with email field instead of password"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    superheroes = models.ManyToManyField(Hero)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
