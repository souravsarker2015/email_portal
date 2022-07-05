from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
