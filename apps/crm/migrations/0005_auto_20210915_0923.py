# Generated by Django 2.2.24 on 2021-09-15 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20210915_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email address'),
        ),
    ]
