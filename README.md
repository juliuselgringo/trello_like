# Taskflow — Trello-like Project Management

Application full-stack pour la gestion collaborative de projets et tâches. Support d'apprentissage Django + Vue.js en profondeur.

**Stack** : Django REST Framework (backend) + Vue.js 3 (frontend) + Tailwind CSS

## 🎯 Contexte pédagogique

Ce projet est un **support d'apprentissage** structuré :
- 📚 Apprendre Django et Vue.js via un cas concret
- 🎨 Maquettes, modèle Merise, base de données fournis
- 👨‍🏫 Accompagnement mentorat (pas auto-génération de code)
- 🔄 Progression par étapes, avec vérifications à chaque point

Voir [.github/copilot-instructions.md](.github/copilot-instructions.md) pour les principes d'accompagnement.

## 📁 Architecture du projet

```
trello_like/
├── .github/
│   └── copilot-instructions.md     # Principes pédagogiques + contexte
├── docs/                           # Tutoriels et documentation
│   ├── tutoDjango1.md
│   ├── tutoDjango2.md
│   └── tutoDjango3.md
├── Maquettes/                      # Designs UI (accueil, dashboard, kanban)
├── Merise/                         # Modèle données + scripts DB
│   ├── scriptTrelloDB.sql
│   ├── trello_like.lo1
│   └── trello_like.loo
├── trello_backend/                 # Django app
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── backDjango/                 # Settings, URLs, WSGI
│   └── projects_app/               # App Django (models, views, serializers)
├── trello_frontend/                # Vue.js app (Vite + Router + Tailwind)
│   ├── README.md                   # 👈 Documentation frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── pages/                  # Login, Dashboard, Kanban
│   │   ├── components/             # Header, OverviewCards, Modales
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   └── .npmrc                      # Sécurité npm (ignore-scripts)
└── README.md                       # 👈 Ce fichier
```

## 🚀 Quick Start

### Backend (Django)

```bash
cd trello_backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server : `http://localhost:8000`

### Frontend (Vue.js)

```bash
cd trello_frontend
npm install
npm run dev
```

App : `http://localhost:5173`

## 📋 État du projet

### ✅ Frontend - Complété

- **Routing** : 5 routes avec lazy-loading
- **Pages**:
  - Login.vue (UI, pas auth)
  - Dashboard.vue (liste projets + modal add/edit)
  - Kanban.vue (colonnes tâches + modales)
- **Composants** :
  - Header, OverviewCards, ModalProject, ModalTask, DeconnexionBtn
- **Design** : Tailwind CSS + variables CSS centralisées
- **Mock data** : Projects, tasks, tags (en ref())

### 🔄 Backend - En cours

- [x] Models Django (auto-générés depuis PostgreSQL) ✅
- [x] Serializers (ProjectSerializer, TaskSerializer) ✅
- [x] ViewSets (ProjectViewSet, TaskViewSet) ✅
- [x] Endpoints testés : GET/POST /api/projects/ ✅
- [ ] Endpoints tâches : compléter tests (CRUD)
- [ ] Authentification (JWT ou session-based)
- [ ] CORS configuration

### 🔗 Intégration frontend ↔ backend

- [ ] Configurer CORS
- [ ] Login : `POST /api/auth/login/` (mock → API)
- [ ] Dashboard : `GET /api/projects/` (mock → API)
- [ ] Kanban : `GET /api/projects/{id}/tasks/` (mock → API)
- [ ] Add project : `POST /api/projects/` (modal emit → API)
- [ ] Add task : `POST /api/projects/{id}/tasks/` (modal emit → API)
- [ ] Edit project : `PUT /api/projects/{id}/` (modal emit → API)
- [ ] Edit task : `PUT /api/tasks/{id}/` (modal emit → API)
- [ ] Drag-drop tâches : `PUT /api/tasks/{id}/` (column_id change)

### 🎁 Bonus (si temps)

- [ ] Drag-drop avec vue-draggable-plus
- [ ] Tags/labels éditables
- [ ] Assignation utilisateurs
- [ ] Responsive design (mobile)
- [ ] Tests (unit + e2e)
- [ ] Permissions (qui peut faire quoi)

## 🏗️ Conventions

### Frontend

- **Composants** : `PascalCase.vue`, réutilisables
- **Pages** : `PascalCase.vue`, dans `src/pages/`
- **Routing** : lazy-loaded avec `() => import()`
- **State** : `ref()` pour le mock, API calls côté page
- **Props** : simples, préférer type-safety
- **Émissions** : `emit()` avec `defineEmits` déclaré

### Backend

- **App Django** : `projects_app`
- **Models** : `Project`, `Task`, `Column`, `Tag`, `User`
- **Views** : ViewSets DRF (CRUD + custom actions)
- **Serializers** : validations + nested relations
- **URLs** : nested routing pour relations

### Base de données

Voir [Merise/scriptTrelloDB.sql](Merise/scriptTrelloDB.sql) pour schema complet.

Principales entités :
- **Project** : project_id, name, description, creation_date
- **Task** : task_id, name, description, deadline, column_id, project_id
- **Column** : column_id (1=À faire, 2=En cours, 3=Fini)
- **Tag** : tag_id, name, color
- **Tagged** : relation many-to-many Task ↔ Tag

## 🔐 Sécurité

### npm

- `.npmrc` avec `ignore-scripts=true` prévient attaques supply chain
- Si dépendance manque un script essential, voir [.github/copilot-instructions.md](.github/copilot-instructions.md#sécurité-npm-et-gestion-des-scripts)

### Django

- CORS configuré pour `localhost:5173` uniquement
- Authentification JWT (ou session) obligatoire
- Serializers valident entrées strictement
- Permissions contrôlent accès resources

## 📚 Documentation supplémentaire

- [trello_frontend/README.md](trello_frontend/README.md) — Frontend détaillé
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — Principes pédagogiques
- [docs/tutoDjango*.md](docs/) — Tutos Django (WIP)
- [Merise/](Merise/) — Modèle données

## 🛠️ Technologies

| Couche | Tech | Version |
|--------|------|---------|
| **Frontend** | Vue.js | 3.x |
| | Vue Router | 4.x |
| | Tailwind CSS | 4.3.3 |
| | Vite | Latest |
| **Backend** | Django | 4.x+ |
| | DRF | 3.x |
| **BD** | SQLite (dev) | Built-in |
| | PostgreSQL (prod) | 12+ |

## 🎓 Prochaines étapes

### Phase 1 : Backend API (semaines 1-2)
1. Modèles Django complets
2. Serializers + ViewSets
3. Routes CRUD projets/tâches
4. Authentification basique

### Phase 2 : Intégration (semaine 3)
1. CORS configuration
2. Frontend → API (remplacer mock data)
3. Drag-drop tâches
4. Login flow complet

### Phase 3 : Finitions (semaine 4)
1. Tests (unit + e2e)
2. Responsive design
3. Permissions avancées
4. Optimisations perf

## 📞 Support

Voir les instructions dans [.github/copilot-instructions.md](.github/copilot-instructions.md) pour l'accompagnement pédagogique.

---

**Démarré** : 2026-08-06 | **Dernière mise à jour** : 2026-08-11
