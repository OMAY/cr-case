from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='profile.png', null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Manager(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='profile.png', null=True, blank=True)

    def __str__(self):
        return self.first_name, self.last_name

#
# class Company(models.Model):
#     name = models.CharField(
#         max_length=100, verbose_name='Название компании')
#     contact = models.CharField(
#         max_length=100, verbose_name='ФИО контактного лица')
#     description = models.TextField(verbose_name='Описание компании')
#     date_of_create = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')
#     date_of_change = models.DateField(default=None, verbose_name='Дата последнего изменения записи')
#     address = models.TextField(verbose_name='Адрес компании')
#     phone = models.CharField(max_length=15, verbose_name='Телефон')
#     email = models.EmailField(max_length=50, verbose_name='Адрес электронной почты')
#     added_manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер, создавший запись')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Компания'
#         verbose_name_plural = 'Компании'
#         ordering = ['date_of_change']
#
#
# class Project(models.Model):
#     name = models.CharField(
#         max_length=100, verbose_name='Название проекта')
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
#     description = models.TextField(verbose_name='Описание проекта')
#     start_date = models.DateField(verbose_name='Дата начала')
#     end_date = models.DateField(verbose_name='Дата окончания')
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость проекта')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Проект'
#         verbose_name_plural = 'Проекты'
#         ordering = ['name']
#
#
# class ContactMessage(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     type_of_message = models.CharField(
#         max_length=100, verbose_name='Канал обращения')
#     manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
#     description = models.TextField(verbose_name='Описание сообщения')
