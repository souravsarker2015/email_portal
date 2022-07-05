from django.contrib import admin

from core.models import Country, State, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']



