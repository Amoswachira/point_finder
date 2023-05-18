from django.db import models
from django.apps import apps

class Point(models.Model):
    coordinates = models.CharField(max_length=255)
    closest_points = models.TextField()

class Meta:
    app_label = apps.get_containing_app_config(__name__).name