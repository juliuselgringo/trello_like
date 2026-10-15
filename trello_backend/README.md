# Trello-like Backend

API Django + DRF qui sert le front Vue.js pour la gestion des projets, colonnes et tâches.

## État actuel

Le backend est fonctionnel pour la phase 1 du projet :
- authentification JWT via cookie HttpOnly
- inscription / connexion / déconnexion
- CRUD des projets
- CRUD des tâches
- lecture des colonnes
- protection des routes par `IsAuthenticated`
- gestion des utilisateurs avec modèle personnalisé

La phase 2 est en cours : refresh token avancé, permissions multi-users, drag & drop Kanban persisté, filtres et notifications.

## Stack

- Python 3.10+
- Django 6
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- SQLite pour le dev local / PostgreSQL compatible en prod

## Structure du projet

```text
trello_backend/
├── backDjango/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── projects_app/
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## Prérequis

- Python 3.10+
- pip
- virtualenv ou venv

## Installation

```bash
cd trello_backend
python -m venv venv
source venv/Scripts/activate   # Windows PowerShell
# ou : venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

## Lancer le serveur

```bash
python manage.py runserver
```

Le backend est alors accessible sur :
- http://127.0.0.1:8000
- http://127.0.0.1:8000/api/

## Variables d’environnement

Le projet lit des variables depuis un `.env` ou l’environnement système :

```env
SECRET_KEY=...
DEBUG=True
DB_NAME=trello_like
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Le projet est compatible avec SQLite pour le développement local, mais la configuration actuelle est orientée PostgreSQL dans `settings.py`.

## Modèle métier

Les modèles principaux sont :
- `User` : utilisateur personnalisé avec `user_name` et `user_email` uniques
- `Project` : projet lié à un utilisateur
- `Column` : colonne Kanban (`column_id`, `column_name`)
- `Task` : tâche avec `task_name`, `task_description`, `task_dead_line`, `column`, `project`
- `Tag` / `Tagged` : tags associés aux tâches

Les règles de validation actuelles :
- `user_name` unique
- `user_email` unique
- `project` et `task` sont associés au projet courant
- `task.column` est la clé qui permet de déplacer la tâche dans une autre colonne

## Authentification

Le backend utilise des JWT stockés dans des cookies HttpOnly.

### Points clés

- le token est envoyé dans le cookie `access_token`
- le navigateur l’envoie automatiquement si `credentials: 'include'` est utilisé côté front
- l’authentification est gérée par `CookieJWTAuthentication`
- chaque route API protectrice exige `IsAuthenticated`

### Login

Route : `POST /api/auth/login/`

Exemple :

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "alice",
    "user_password": "secret123"
  }'
```

Réponse :
- cookie `access_token` reçu automatiquement par le navigateur
- body JSON de confirmation

### Register

Route : `POST /api/auth/register/`

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "alice",
    "user_email": "alice@example.com",
    "user_password": "secret123"
  }'
```

### Logout

Route : `POST /api/auth/logout/`

Le cookie est supprimé côté backend.

### Utilisateur courant

Route : `GET /api/user/me/`

Retourne les infos de l’utilisateur connecté.

## API actuelle

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/user/me/`

### Projets

- `GET /api/projects/`
- `GET /api/projects/{id}/`
- `POST /api/projects/`
- `PUT /api/projects/{id}/`
- `PATCH /api/projects/{id}/`
- `DELETE /api/projects/{id}/`

Exemple de création :

```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Nouveau projet",
    "project_description": "Description",
    "project_creation_date": "2026-08-22",
    "user": 1
  }'
```

### Tâches

- `GET /api/tasks/`
- `GET /api/tasks/?project_id={id}`
- `GET /api/tasks/{id}/`
- `POST /api/tasks/`
- `PUT /api/tasks/{id}/`
- `PATCH /api/tasks/{id}/`
- `DELETE /api/tasks/{id}/`

Exemple de récupération des tâches d’un projet :

```bash
curl "http://localhost:8000/api/tasks/?project_id=1"
```

### Colonnes

- `GET /api/columns/`
- `GET /api/columns/{id}/`

## CORS et frontend

La configuration actuelle autorise le frontend Vue sur :

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]
CORS_ALLOW_CREDENTIALS = True
```

Important : pour que le navigateur envoie les cookies, le frontend doit utiliser :

```js
fetch(url, {
  credentials: 'include'
})
```

## Points de vigilance

- Les URLs de l’API utilisent bien les trailing slashes côté frontend (`/api/projects/{id}/`, `/api/tasks/{id}/`).
- Les points d’entrée de l’API ne doivent pas être appelés sans `credentials: 'include'`.
- Les modèles utilisent une clé métier personnalisée (`task_id`, `project_id`, etc.) qui est renvoyée côté front.

## Prochaines étapes

1. Refresh token avec rotation automatique
2. Permissions multi-user / collaborateurs
3. Drag & drop Kanban persisté en base
4. Filtres de recherche et statuts
5. Tests Django
6. Notifications temps réel

## Bonnes pratiques d’utilisation

- Toujours passer par le frontend pour authentifier les requêtes
- Vérifier les réponses HTTP avant de modifier l’état local
- respecter la convention des trailing slashes
- utiliser les objets JSON renvoyés par l’API pour mettre à jour l’état Vue

## Référence rapide

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/user/me/
GET  /api/projects/
POST /api/projects/
GET  /api/tasks/?project_id={id}
POST /api/tasks/
GET  /api/columns/
```

|---------|-----|--------|
| GET | /api/projects/ | Lister |
| POST | /api/projects/ | Créer |
| GET | /api/projects/{id}/ | Détail |
| PUT | /api/projects/{id}/ | Remplacer |
| PATCH | /api/projects/{id}/ | Modifier partiellement |
| DELETE | /api/projects/{id}/ | Supprimer |

## ⚙️ Stack

- **Django 6.0** : Web framework
- **Django REST Framework** : REST API + serializers + viewsets
- **PostgreSQL 14** : Base de données
- **psycopg2** : Adaptateur PostgreSQL

## 📝 Notes pédagogiques

### Pourquoi ce pattern ?

- **DRY** (Don't Repeat Yourself) : ModelViewSet génère CRUD automatiquement
- **Cohérence** : tous les endpoints suivent le même pattern
- **Extensibilité** : facile d'ajouter des actions custom

### Pièges courants

⚠️ **Les champs non-nullables du modèle doivent être dans le serializer**, sinon Django lève une IntegrityError.  
Exemple : si `user` est `NOT NULL`, il faut l'inclure dans `fields` même si l'API ne le crée pas.

⚠️ **Tester incrémentalement** : chaque endpoint doit être testé avant de passer au suivant.

## 🚦 Prochaines étapes

- [ ] Tester tous endpoints Task (GET, POST, PUT, PATCH, DELETE)
- [ ] Ajouter authentification (JWT ou session)
- [ ] Configurer CORS pour le frontend
- [ ] Ajouter validations métier
- [ ] Tests unitaires
