# Generated by Django 5.0.2 on 2024-02-27 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('web_Backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='User_Registrations',
        ),
    ]
