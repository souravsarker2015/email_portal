import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from core.models import BaseModel
from core.models import Country, State, City
import secrets


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.username


class Recipient(BaseModel):
    name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=200, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, max_length=50, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True, default=datetime.now)

    @property
    def age(self):
        return int((datetime.now().date() - self.dob).days / 365)

    def __str__(self):
        return self.email_address


class Email(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    subject = models.CharField(max_length=500, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject


class EmailRecipient(BaseModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True, blank=True, related_name="email_er")
    recipient = models.ForeignKey(Recipient, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="recipient_er")
    email_address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class History(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    subject = models.CharField(max_length=100, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject


class Schedule(BaseModel):
    schedule_title = models.CharField(max_length=254, null=True, blank=True)
    date_time = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def __str__(self):
        return self.schedule_title


class Filter(BaseModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.JSONField(default=list)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Csv(models.Model):
    file_name = models.FileField(upload_to="csvs")
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class ScheduleContent(BaseModel):
    email = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=254, null=True, blank=True)
    schedule = models.CharField(max_length=254, null=True, blank=True)

# def default_filter():
#     return [
#         {
#             "op": "",
#             "column": "age",
#             "eql": "is",
#             "value": "18"
#         },
#         {
#             "op": "OR",
#             "column": "country",
#             "eql": "is",
#             "value": ["bangladesh"]
#         },
#         {
#             "op": "AND",
#             "column": "state",
#             "eql": "is",
#             "value": ["dhaka", "chattagram"]
#         },
#         {
#             "op": "AND",
#             "column": "state",
#             "eql": "is",
#             "value": ["dhaka", "chattagram"]
#         },
#
#     ]
# class YourModel(models.Model):
#     key = models.CharField(
#         _("Key for email tracking"), max_length=255, default=secrets.token_hex(10))
#     seen_at = models.DateTimeField(null=True, blank=True)
#     request = models.TextField(null=True, blank=True)
