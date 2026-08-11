# Dotenv, CORS

## Dotenv

1. Installer dotenv dans venv
```
venv/Scripts/activate

python -m pip install python-dotenv
```

2. Dans backdjango/settings.py ajouter
```
import os
from dotenv import load_dotenv

load_dotenv()
```

## CORS

1. installer django-cors-headers
```
python -m pip install django-cors-headers
```

2. modifier backDjango/settings.py

- 'corsheaders' ajouté à INSTALLED_APPS
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'projects_app',

]
```

- Middleware CORS placé AVANT CommonMiddleware (ordre critique!)
```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

- localhost:5173 autorisé dans CORS_ALLOWED_ORIGINS
```
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Frontend Vue.js dev server
]
```
