# Trello-like Frontend

Application Vue 3 pour la gestion de projets, tâches et colonnes Kanban.

## État actuel

Le frontend est fonctionnel pour la majeure partie de la phase 1 :
- page de connexion et inscription
- dashboard avec liste des projets
- page Kanban avec colonnes et tâches
- modal de création / édition de projet et de tâche
- déconnexion avec suppression du cookie JWT
- intégration des appels API avec `credentials: 'include'`
- gestion simple des erreurs API et redirection de session

Le drag & drop entre colonnes est en cours d’implémentation et est déjà branché sur les événements du composant draggable, mais la persistance côté backend reste à finaliser selon le flux métier de la tâche.

## Stack

- Vue 3
- Vite
- Vue Router 4
- Tailwind CSS
- JavaScript ES modules

## Structure du projet

```text
trello_frontend/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── App.vue
│   ├── main.js
│   ├── style.css
│   ├── components/
│   │   ├── DeconnexionBtn.vue
│   │   ├── Header.vue
│   │   ├── KanbanArray.vue
│   │   ├── ModalProject.vue
│   │   ├── ModalSignIn.vue
│   │   ├── ModalTask.vue
│   │   ├── OverviewCards.vue
│   │   └── ProjectsArray.vue
│   ├── composables/
│   │   └── useProjectTasks.js
│   ├── pages/
│   │   ├── Dashboard.vue
│   │   ├── Kanban.vue
│   │   └── Login.vue
│   └── router/
│       └── index.js
└── README.md
```

## Prérequis

- Node.js 18+
- npm
- backend Django lancé sur http://localhost:8000

## Installation

```bash
cd trello_frontend
npm install
```

## Lancer le projet

```bash
npm run dev
```

L’application est disponible sur :
- http://localhost:5173

## Sécurité npm

Le projet contient un `.npmrc` avec `ignore-scripts=true` pour limiter les risques de scripts malveillants exécutés pendant l’installation des dépendances.

Si une dépendance nécessite un script d’installation spécifique, il faut faire une exception explicite et documenter la raison.

## Routes de l’application

```text
/            -> redirection vers /login
/login       -> Login.vue
/dashboard   -> Dashboard.vue
/kanban      -> Kanban.vue
```

La configuration se trouve dans :

```js
src/router/index.js
```

## Authentification

Le frontend utilise le cookie HttpOnly `access_token` envoyé par le backend Django.

### Règle clé

Les appels HTTP doivent utiliser :

```js
fetch(url, {
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
  },
})
```

Cela permet au navigateur d’envoyer le cookie sur les requêtes protégées.

### Workflow actuel

1. L’utilisateur soumet le formulaire de connexion
2. `POST /api/auth/login/`
3. le backend renvoie le cookie JWT
4. le navigateur se redirige vers `/dashboard`
5. les écrans fetchent ensuite les projets / tâches avec `credentials: include`

## API utilisée par le frontend

### Authentification

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/user/me/`

### Projets

- `GET /api/projects/`
- `GET /api/projects/{id}/`
- `POST /api/projects/`
- `PUT /api/projects/{id}/`
- `DELETE /api/projects/{id}/`

### Tâches

- `GET /api/tasks/?project_id={id}`
- `GET /api/tasks/{id}/`
- `POST /api/tasks/`
- `PUT /api/tasks/{id}/`
- `DELETE /api/tasks/{id}/`

### Colonnes

- `GET /api/columns/`

## Fonctionnalités implémentées

### Login

- formulaire utilisateur / mot de passe
- appel vers `/api/auth/login/`
- redirection vers `/dashboard`

### Dashboard

- affichage des projets
- création et modification de projet
- recherche dans la liste des projets
- vues de synthèse via `OverviewCards`

### Kanban

- affichage des colonnes et des tâches
- ouverture de modal pour créer / modifier une tâche
- suppression de tâche
- drag & drop entre colonnes : en cours d’implémentation côté logique métier

### Déconnexion

- bouton `DeconnexionBtn`
- appel vers `/api/auth/logout/`
- suppression du cookie navigateur
- redirection vers `/login`

## Composants principaux

### `Header.vue`
Bandeau réutilisable sur les écrans principaux.

### `OverviewCards.vue`
Cartes de synthèse (projets, tâches, retards, etc.).

### `ModalProject.vue`
Modal de création / édition d’un projet.

### `ModalTask.vue`
Modal de création / édition d’une tâche.

### `KanbanArray.vue`
Conteneur des colonnes Kanban et logique d’affichage des cartes.

## Design / style

Le style global est centralisé dans `src/style.css` avec :
- variables CSS pour les couleurs
- fond principal
- thèmes de composants
- palette de tags et de colonnes

La page est pensée pour rester lisible sur desktop tout en gardant un comportement responsive.

## Bonnes pratiques du front

- Utiliser `credentials: 'include'` sur tous les appels sécurisés
- Vérifier le `response.ok` avant d’utiliser les données
- Gérer les erreurs de manière explicite dans le `catch`
- Respecter les URLs API avec trailing slash
- Ne pas utiliser de `column_id` depuis le front si le backend attend `column`

## Prochaines étapes

1. Finaliser le drag & drop entre colonnes avec mise à jour de `task.column`
2. Faire le `PUT` sur `/api/tasks/{id}/` après chaque drop
3. Gérer le rollback visuel si l’API échoue
4. Ajouter filtres / recherche avancée
5. Ajouter refresh token + gestion d’expiration plus robuste
6. Ajouter tests E2E sur les flux login / dashboard / kanban

## Points pédagogiques

Ce projet est un support d’apprentissage pour comprendre :
- architecture Django + Vue
- relation front/back via API
- authentification cookie JWT
- composants Vue et state local
- navigation entre pages via `vue-router`
- logique Kanban et drag & drop

## Référence rapide

```text
/login
/dashboard
/kanban
```

```text
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/logout/
GET  /api/projects/
GET  /api/tasks/?project_id={id}
GET  /api/columns/
PUT  /api/tasks/{id}/
```

- [ ] Tests (unit + e2e si temps)

## 📚 Références

- [Vue.js 3 docs](https://vuejs.org/)
- [Vue Router 4 docs](https://router.vuejs.org/)
- [Tailwind CSS docs](https://tailwindcss.com/)
- [Vite docs](https://vitejs.dev/)
