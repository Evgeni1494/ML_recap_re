from django.db import models
from datetime import date

class RealFilmData(models.Model):
    title = models.CharField(max_length=200, default="Titre par défaut")
    box_office = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    genre = models.CharField(max_length=100, default="Genre par défaut")
    actors = models.CharField(max_length=500, default="Acteurs par défaut")
    prediction = models.IntegerField(default=0)  # Colonne pour le nombre d'entrées estimé
    confiance = models.FloatField(default=0.0)  # Colonne pour la valeur de confiance
    date = models.DateField(default=date.today)  # Colonne pour la date avec la date d'aujourd'hui par défaut
    
    def __str__(self):
        return self.title

