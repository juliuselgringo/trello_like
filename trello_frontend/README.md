# Trello-like Frontend

Application Vue.js 3 pour la gestion de projets et tâches en style Kanban.

## 🚀 Setup

### Prérequis
- Node.js 18+ 
- npm 9+

### Installation

```bash
cd trello_frontend
npm install
```

**⚠️ Sécurité npm** : Le fichier `.npmrc` contient `ignore-scripts=true` pour prévenir les attaques supply chain. Si un package essential manque après installation, voir [../.github/copilot-instructions.md](../.github/copilot-instructions.md#sécurité-npm-et-gestion-des-scripts).

### Démarrage dev

```bash
npm run dev
```

Application accessible à `http://localhost:5173`

## 📁 Structure

```
src/
  ├── App.vue              # Root component avec RouterView
  ├── main.js              # Initialisation Vue + router
  ├── style.css            # Styles globaux, variables CSS, Tailwind
  ├── router/
  │   └── index.js         # Configuration routes (vue-router 4)
  ├── pages/               # Composants pages (lazy-loaded)
  │   ├── Login.vue        # Page authentification
  │   ├── Dashboard.vue    # Liste projets + modal ajout/edit
  │   └── Kanban.vue       # Suivi tâches + modal ajout/edit
  ├── components/          # Composants réutilisables
  │   ├── Header.vue       # Logo + titre
  │   ├── OverviewCards.vue # Stats cards
  │   ├── ModalProject.vue # Modal add/edit projet
  │   ├── ModalTask.vue    # Modal add/edit tâche
  │   └── DeconnexionBtn.vue # Bouton logout
  └── public/              # Assets statiques
```

## 🎨 Design System

### Couleurs (CSS Variables)

Définies dans `src/style.css`:
```css
--gradient-main: linear-gradient(135deg, #a855f7 10%, #000000 50%)
--input-bg: rgb(48, 46, 46)
--text-primary: #ffffff
--accent-purple: #a855f7
```

### Palette Tags

5 couleurs cycliques pour badges projets :
- `text-purple-500`, `text-yellow-500`, `text-green-500`, `text-red-500`, `text-blue-500`

## 🛣️ Routes

| Route | Component | Statut |
|-------|-----------|--------|
| `/` | → `/login` (redirect) | ✅ Impl. |
| `/login` | Login.vue | ✅ Impl. (mock) |
| `/dashboard` | Dashboard.vue | ✅ Impl. (mock data) |
| `/kanban` | Kanban.vue | ✅ Impl. (mock data) |

Chaque route utilise **lazy-loading** :
```javascript
() => import('../pages/PageName.vue')
```

## 🧩 Composants clés

### Header.vue
Logo + "Taskflow" title. Réutilisé dans Login, Dashboard, Kanban.

**Props** : aucune

```vue
<Header />
```

### OverviewCards.vue
Affiche une stat avec label + valeur, couleur dynamique.

**Props** :
- `label` (String) : "Projet Actifs", "Tâches en cours", etc.
- `value` (String | Number) : valeur à afficher

**Exemple** :
```vue
<OverviewCards label="Projet Actifs" :value="5" />
```

### ModalProject.vue (Upsert)
Modal pour ajouter/modifier un projet. Mode déterminé par prop `mode`.

**Props** :
- `mode` (String) : `'add'` ou `'edit'`
- `project` (Object) : optionnel, données pré-remplies si edit

**Événements émis** :
- `@create` : mode add, payload = `{ project_name, project_description, project_creation_date }`
- `@update` : mode edit, payload = `{ project_id, project_name, ... }`
- `@cancel` : fermeture sans action

**Exemple** :
```vue
<ModalProject 
  :mode="mode" 
  :project="selectedProject" 
  @create="handleCreate" 
  @update="handleUpdate" 
  @cancel="closeModal"
/>
```

### ModalTask.vue (Upsert)
Modal pour ajouter/modifier une tâche (sans choix colonne, drag-drop gère ça).

**Props** :
- `mode` (String) : `'add'` ou `'edit'`
- `task` (Object) : optionnel
- `project` (Object) : project courant (requis pour defaults)

**Événements émis** :
- `@create` : payload = `{ task_name, task_description, task_dead_line, column_id: 1, project_id }`
- `@update` : payload = `{ task_id, task_name, ... }`
- `@cancel`

## 🔌 Intégration API (TODO)

Actuellement : **mock data** en `ref()`. À remplacer par `fetch()` vers Django backend.

### Endpoints attendus

```
GET    /api/projects/                  # Lister projets
POST   /api/projects/                  # Créer projet
PUT    /api/projects/{id}/             # Modifier projet
DELETE /api/projects/{id}/             # Supprimer projet

GET    /api/projects/{id}/tasks/       # Lister tâches projet
POST   /api/projects/{id}/tasks/       # Créer tâche
PUT    /api/tasks/{id}/                # Modifier tâche (colonne, etc.)
DELETE /api/tasks/{id}/                # Supprimer tâche
```

## 🛠️ Technologies

- **Vue.js 3** (Composition API, `<script setup>`)
- **Vue Router 4** (lazy-loading, client-side routing)
- **Tailwind CSS 4.3.3** (@tailwindcss/vite plugin)
- **Vite** (build tool, dev server)
- **npm** (package manager, sécurisé avec ignore-scripts)

## 📝 Notes pédagogiques

- **Pas de Pinia/state global** : mock data suffit pour le moment
- **Pas de composants slots complexes** : préférer props simples
- **Drag-drop** : implémenté plus tard avec events natifs ou lib externe
- **Formulaires** : validation côté UI uniquement, backend fera validation stricte

## 🚦 Checklist prochaines étapes

- [ ] Configurer CORS Django
- [ ] Implémenter login avec JWT/session
- [ ] Connecter Dashboard → API projets
- [ ] Connecter Kanban → API tâches
- [ ] Implémenter drag-drop tâches (avec PUT /api/tasks/{id}/)
- [ ] Styling responsif (mobile)
- [ ] Tests (unit + e2e si temps)

## 📚 Références

- [Vue.js 3 docs](https://vuejs.org/)
- [Vue Router 4 docs](https://router.vuejs.org/)
- [Tailwind CSS docs](https://tailwindcss.com/)
- [Vite docs](https://vitejs.dev/)
