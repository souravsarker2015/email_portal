# Generated by Django 4.0.5 on 2022-07-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0002_schedule_created_schedule_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=254, null=True)),
                ('schedule', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
