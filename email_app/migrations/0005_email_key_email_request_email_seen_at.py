# Generated by Django 4.0.5 on 2022-07-04 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0004_rename_storage_schedulecontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='key',
            field=models.CharField(default='e65d36d750a929c3a812', max_length=255, verbose_name='Key for email tracking'),
        ),
        migrations.AddField(
            model_name='email',
            name='request',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='seen_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]