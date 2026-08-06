# Installation djangorestframework et création de Serializer - viewsets - urls

## Installation djangorestframework 

1. Commande pip d'installation
```
python -m pip install djangorestframework
```

2. Ajoutez 'rest_framework' dans INSTALLED_APPS dans backDjango/settings.py (après les apps Django officielles, avant projects_app)

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
    'projects_app'
]
```

3. On vérifie que tout est ok avec 
```
python manage.py check
```

## Création de Serializer

Serializer va permettre de transformer les modèles Django en JSON et inversement pour les requêtes et les réponses
Crée trello_backend/serializers.py

## Création de viewsets

La viewset est la "logique métier" de l'API. Elle dit : "Quand quelqu'un arrive sur GET /projects, retourne tous les projets sérialisés en JSON".
Fichier à créer/modifier : projects_app/views.py

## Création urls

1. Crée projects_app/urls.py (s'il n'existe pas)

2. Puis dans backDjango/urls.py :

Importe include de django.urls (s'il n'est pas déjà là)
Ajoute cette ligne dans urlpatterns :
```
path('api/', include('projects_app.urls')),
```

3. Tester 
- lancer le serveur
```
python manage.py runserver
```
- consulter l'adresse dans browser:
http://127.0.0.1:8000/api/projects/

## Les endpoints auto

```
⚠️ Attention : N'oublie pas d'ajouter tous les champs requis dans fields du serializer, sinon DRF les ignorera et Django lèvera une IntegrityError.

Exemple : si user est obligatoire en base, il faut le mettre dans fields du serializer.
```

GET /projects/{projects_id} à tester avec
http://127.0.0.1:8000/api/projects/1/
dans le browser.

POST à tester dans bash avec curl
```
curl.exe -X POST http://127.0.0.1:8000/api/projects/ -H "Content-Type: application/json" -d '{"project_name": "Mon nouveau projet", "project_description": "Test", "project_creation_date": "2026-07-23", "user": 1}' -s | head -50
```

ModelViewSet génère automatiquement tous les endpoints CRUD :

| Méthode | URL |Action |
|---------|-----|-------|
| GET | api/projects/ |	Lister tous |
| POST | /api/projects/ |	Créer un |
| GET |	/api/projects/{id}/	| Récupérer UN |
| PUT | /api/projects/{id}/	| Remplacer complètement |
| PATCH | /api/projects/{id}/ | Modifier partiellement |
| DELETE | /api/projects/{id}/ | Supprimer |

Différence :

- PUT : remplace tout le projet (tous les champs obligatoires)
- PATCH : modifie juste les champs envoyés
- DELETE : supprime le projet

Exemple PUT (remplacer entièrement) :
```
curl.exe -X PUT http://127.0.0.1:8000/api/projects/1/ -H "Content-Type: application/json" -d '{"project_name": "Nouveau nom", "project_description": "Nouvelle desc", "project_creation_date": "2026-07-23", "user": 1}'
```

Exemple DELETE (supprimer) :
```
curl.exe -X DELETE http://127.0.0.1:8000/api/projects/1/
```

Exemple PATCH (modifier juste le nom) :
```
curl.exe -X PATCH http://127.0.0.1:8000/api/projects/1/ -H "Content-Type: application/json" -d '{"project_name": "Nouveau nom"}'
```
## Petit cours de curl

|Flag|	Signification|	Exemple |
|----|---------------|----------|
|-X	| Method — méthode HTTP (GET, POST, PUT, DELETE, PATCH)|	-X POST |
|-H	| Header — ajouter un en-tête |	-H "Content-Type: application/json" |
|-d | Data — données à envoyer dans le body | -d '{"name": "test"}'
|-s | Silent — mode silencieux (pas d'infos de progression)	| -s