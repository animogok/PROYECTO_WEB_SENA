# Generated by Django 5.0.2 on 2024-02-28 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_Backend', '0008_alter_user_registrations_firsname_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user_registrations',
            table='users',
        ),
    ]