# Generated by Django 5.0.2 on 2024-02-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_Backend', '0003_user_registrations_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_registrations',
            name='birth_date',
            field=models.DateField(default='1000/01/01'),
        ),
    ]