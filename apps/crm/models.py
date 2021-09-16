from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        null=True,
        blank=True,
        unique=False,
    )
    profile_picture = models.ImageField(default='profile.png', null=True, blank=True, verbose_name='Фото пользователя')
    is_manager = models.BooleanField(default=False, verbose_name='Пользователь-менеджер')

    objects = MyUserManager()

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название компании')
    contact = models.CharField(
        max_length=100, verbose_name='ФИО контактного лица')
    sh_description = models.TextField(default='', verbose_name='Краткое описание компании')
    description = models.TextField(verbose_name='Полное описание компании')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    date_of_change = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения записи')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес компании')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Номер телефона')
    ad_phone_1 = models.CharField(max_length=15, null=True, blank=True, verbose_name='Дополнительный номер телефона 1')
    ad_phone_2 = models.CharField(max_length=15, null=True, blank=True, verbose_name='Дополнительный номер телефона 2')
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name='Адрес электронной почты', )

    ad_email_1 = models.EmailField(max_length=50, null=True, blank=True,
                                   verbose_name='Дополнительный адрес электронной почты 1')
    ad_email_2 = models.EmailField(max_length=50, null=True, blank=True,
                                   verbose_name='Дополнительный адрес электронной почты 2')
    created_by = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='comp_create',
                                   verbose_name='Создал')
    updated_by = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='comp_update',
                                   verbose_name='Изменил')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['date_of_change']


class Project(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название проекта')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание проекта')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость проекта')
    created_by = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='proj_create',
                                   verbose_name='Создал')
    updated_by = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='proj_update',
                                   verbose_name='Изменил')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['name']

#
# class ContactMessage(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     type_of_message = models.CharField(
#         max_length=100, verbose_name='Канал обращения')
#     manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
#     description = models.TextField(verbose_name='Описание сообщения')
