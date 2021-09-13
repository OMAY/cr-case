from django.contrib.auth.models import User
from django.db import models

class Company(models.Model):
    ...

class Company(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название компании')
    contact = models.CharField(
        max_length=100, verbose_name='ФИО контактного лица')
    description = models.TextField(verbose_name='Описание компании')
    date_of_create = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')
    date_of_change = models.DateField(default=None, verbose_name='Дата последнего изменения записи')
    address = models.TextField(verbose_name='Адрес компании')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(max_length=50, verbose_name='Адрес электронной почты')

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
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['name']


class ContactMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type_of_message = models.CharField(
        max_length=100, verbose_name='Канал обращения')
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание сообщения')
