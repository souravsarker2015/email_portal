# Generated by Django 4.0.5 on 2022-07-03 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0003_storage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Storage',
            new_name='ScheduleContent',
        ),
    ]
