# Installation Django et ORM

## .venv

Création de l'environnement virtuel
```
python -m venv venv
```

Activation de l'env
```
./venv/Scripts/Activate.ps1
```

## Django

1. Aller dans le dossier dédié (ici trello_backend)
```
cd trello_backend
```

2. Installer Django avec pip
```
python -m pip install Django
```

3. Vérifier la version
```
python -m django --version
```

4. Démarrer le projet (ici on démarre le projet dans dossier backDjango dans le dossier courant trello_backend)
```
django-admin startproject backDjango .
```

5. Création du fichier requirements.txt 
```
python -m pip freeze > requirements.txt
```

6. Vérification du bon fonctionnement du serveur
```
python manage.py runserver
```

7. Créer une app dans le dossier courant (ici trello_backend et l'app est projects_app)
```
python manage.py startapp projects_app
```
Le nom de l'app doit correspondre à une application métier. (Pas très clair pour l'instant à voir plus tard)

8. Ajouter ce nom d'app dans settings.py du dossier où est démarré le projet (ici backDjango)

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects_app'
]
```

9. Vérifier que Django détecte l'app créé
```
python manage.py check
```
résutat attendu: System check identified no issues (0 silenced).

## Installation de l'ORM 

1. Installation psycopg
```
python -m pip install "psycopg[binary]"
```

2. Ajout des infos concernant la database
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trellodb',
        'USER': 'postgres',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

3. Générer des modèles à partir de la database
```
python manage.py inspectdb | Out-File -FilePath .\projects_app\models.py -Encoding utf8
```

4. Si tu modifies la database, met à jour models.py

````
python manage.py inspectdb > projects_app/models.py
```