from django.contrib import admin

from .models import HydroponicSystem, Measurement


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'description')


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('system', 'ph', 'water_temperature', 'tds', 'created_at')
    list_filter = ('created_at', 'system')
    search_fields = ('system__name',)
