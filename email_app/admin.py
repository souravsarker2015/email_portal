from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipient, Email, History, EmailRecipient, Filter, Csv, Schedule, ScheduleContent, TrackedRecipients
from email_app.forms import CustomUserForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserForm
    form = CustomUserChangeForm
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email_address', 'country', 'state', 'city', 'dob', 'updated', 'created']


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'subject', 'email_body']


# @admin.register(EmailRecipient)
# class EmailRecipientAdmin(admin.ModelAdmin):
#     list_display = ['id', ]


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_by']


@admin.register(History)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'email', 'body']


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'uploaded', 'activated']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'schedule_title', 'date_time']


@admin.register(ScheduleContent)
class ScheduleContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'subject', 'schedule']


@admin.register(TrackedRecipients)
class TrackedRecipientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'subject', 'seen_time']
