# Trello-like Backend

API REST avec Django et Django REST Framework pour la gestion de projets et tâches.

## 🚀 Setup

### Prérequis
- Python 3.10+
- PostgreSQL 14+ (base `trellodb`)
- pip, venv

### Installation

```bash
cd trello_backend

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Migrations (données déjà en place)
python manage.py migrate

# Vérifier la config
python manage.py check
```

### Démarrage dev

```bash
python manage.py runserver
```

Server : `http://127.0.0.1:8000`  
Browsable API : `http://127.0.0.1:8000/api/`

## 📁 Structure

```
backDjango/               # Projet Django (settings, URLs, WSGI)
│   ├── settings.py       # Config (INSTALLED_APPS, DB, etc.)
│   ├── urls.py           # URLs principales
│   ├── asgi.py
│   └── wsgi.py
│
projects_app/             # App Django (métier)
│   ├── models.py         # Project, Task, Column, Tag, User (auto-générés)
│   ├── serializers.py    # ProjectSerializer, TaskSerializer (JSON ↔ Model)
│   ├── views.py          # ProjectViewSet, TaskViewSet (CRUD)
│   ├── urls.py           # Routing DRF avec DefaultRouter
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   └── __init__.py
│
manage.py                 # CLI Django
requirements.txt          # Dépendances
db.sqlite3               # BD local (dev)
```

## 🔌 Endpoints implémentés

### Projects

**GET** `/api/projects/`  
Lister tous les projets.

```bash
curl http://127.0.0.1:8000/api/projects/ -s | python -m json.tool
```

Response:
```json
[
  {
    "project_id": 1,
    "project_name": "Roadmap Q3",
    "project_description": "Planif Q3 2026",
    "project_creation_date": "2026-07-15",
    "user": 1
  },
  ...
]
```

---

**GET** `/api/projects/{id}/`  
Récupérer un projet.

```bash
curl http://127.0.0.1:8000/api/projects/1/ -s | python -m json.tool
```

---

**POST** `/api/projects/`  
Créer un projet.

```bash
curl.exe -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Mon projet", "project_description": "Test", "project_creation_date": "2026-08-11", "user": 1}' \
  -s | python -m json.tool
```

---

**PUT** `/api/projects/{id}/`  
Remplacer complètement un projet.

```bash
curl.exe -X PUT http://127.0.0.1:8000/api/projects/1/ \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Nouveau nom", "project_description": "Desc", "project_creation_date": "2026-08-11", "user": 1}' \
  -s | python -m json.tool
```

---

**PATCH** `/api/projects/{id}/`  
Modifier partiellement un projet.

```bash
curl.exe -X PATCH http://127.0.0.1:8000/api/projects/1/ \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Nouveau nom"}' \
  -s
```

---

**DELETE** `/api/projects/{id}/`  
Supprimer un projet.

```bash
curl.exe -X DELETE http://127.0.0.1:8000/api/projects/1/ -s
```

---

### Tasks

**GET** `/api/tasks/`  
Lister toutes les tâches.

```bash
curl http://127.0.0.1:8000/api/tasks/ -s | python -m json.tool
```

---

**POST** `/api/tasks/`  
Créer une tâche.

```bash
curl.exe -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"task_name": "Ma tâche", "task_description": "Faire un truc", "task_dead_line": "2026-08-15", "column": 1, "project": 1}' \
  -s | python -m json.tool
```

---

## 🏗️ Architecture DRF

Pattern établi : **Serializer → ViewSet → Router**

1. **Serializer** (`serializers.py`) : transforme modèles Django ↔ JSON
   ```python
   class ProjectSerializer(serializers.ModelSerializer):
       class Meta:
           model = Project
           fields = ['project_id', 'project_name', ...]
   ```

2. **ViewSet** (`views.py`) : logique métier, génère automatiquement CRUD
   ```python
   class ProjectViewSet(viewsets.ModelViewSet):
       queryset = Project.objects.all()
       serializer_class = ProjectSerializer
   ```

3. **Router** (`urls.py`) : génère URLs automatiquement
   ```python
   router.register(r'projects', ProjectViewSet)
   ```

**Endpoints auto-générés par ModelViewSet** :
| Méthode | URL | Action |
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
