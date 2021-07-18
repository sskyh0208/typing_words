from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse_lazy
from datetime import date, datetime, timedelta
from uuid import uuid4

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email.')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, verbose_name='ユーザ名')
    email = models.CharField(max_length=255, unique=True, verbose_name='メールアドレス')
    is_active = models.BooleanField(default=False, verbose_name='アカウントの有効化')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'ユーザ'

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')


class PasswordRestTokenManager(models.Manager):
    def get_user(self, token):
        now = datetime.now()
        query_set = self.get_queryset().filter(token=token, expaire_at__gt=now).first()
        return query_set.user if query_set else None

    def publish_token(self, user):
        token = str(uuid4())
        reset_token = self.model(
            token=token,
            user=user,
            # 24時間後まで期限を設ける
            expaire_at=datetime.now() + timedelta(days=1)
        )
        reset_token.save(using=self.db)
        return token


class PasswordRestToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(default=datetime.now())
    expaire_at = models.DateTimeField(default=datetime.now())

    objects = PasswordRestTokenManager()