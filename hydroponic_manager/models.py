from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Measurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE)
    ph = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(14.0),
        ]
    )
    tds = models.PositiveIntegerField()
    water_temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
