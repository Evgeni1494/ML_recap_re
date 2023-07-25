from django.db import models
from datetime import date

class ModelMetrics(models.Model):
    Metrique = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title