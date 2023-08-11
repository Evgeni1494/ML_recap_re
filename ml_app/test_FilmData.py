# create_film.py
import os
import django

# Définir le nom de votre projet Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ml_app.settings")
django.setup()

from user_app.models import FilmData

def create_film_entry():
    film_data = {
        "title": "Titre du film 11",
        "box_office": 11000000.00,
        "genre": "Action",
        "actors": "Acteur 1, Acteur 2",
        "prediction": 110000,
        "confiance": 0.11,
    }

    film = FilmData(**film_data)
    film.save()

if __name__ == "__main__":
    create_film_entry()

