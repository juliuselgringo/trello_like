# Contexte du projet

Ce projet est un support d'apprentissage pour progresser vers les frameworks.

- Objectif principal: apprendre Django et Vue.js en profondeur.
- Contrainte pedagogique: ne pas coder a la place de l'etudiante.
- Materiel deja disponible: maquettes, modele Merise, base de donnees, projet Vue deja initialise dans `trello_frontend/`.

## État du projet (2026-08-22)

### Frontend ✅
- ✅ Routing 4 routes (/, /login, /dashboard, /kanban) avec lazy-loading
- ✅ Pages : Login.vue, Dashboard.vue (liste projets + modales), Kanban.vue (colonnes + modales)
- ✅ Composants réutilisables : Header, OverviewCards, ModalProject, ModalTask, DeconnexionBtn
- ✅ Design complet avec Tailwind CSS + variables CSS centralisées
- ✅ Responsive avec Flex/Grid (colonnes wrap sur petit écran)
- ✅ Login.vue : intégration `/api/auth/login/` + redirection vers dashboard
- ✅ Dashboard.vue + Kanban.vue : fetch avec `credentials: 'include'` + trailing slash `/api/projects/{id}/`
- ✅ Bouton Déconnexion : appel `/api/auth/logout/` + suppression cookie + redirection login
- ✅ Intercepteur global (`fetchWithAuth`) : gère 401/403 → déconnexion automatique

### Backend ✅ (Phase 1 Complétée)
- ✅ Models Django (Project, Task, Column, Tag, User — fields incluent user_name)
- ✅ Serializers DRF (ProjectSerializer avec `read_only_fields`, TaskSerializer avec nested Tags)
- ✅ ViewSets (ProjectViewSet, TaskViewSet avec IsAuthenticated permission)
- ✅ Endpoints GET/POST/PUT/DELETE /api/projects/ et /api/tasks/
- ✅ **Authentification JWT** :
  - LoginView (POST /api/auth/login/) → JWT HttpOnly cookie (1 min)
  - RegisterView (POST /api/auth/register/) → crée user avec password hashé + validation unique
  - LogoutView (POST /api/auth/logout/) → supprime cookie (authentification_classes=[], permission_classes=[])
  - Protection : tous endpoints nécessitent IsAuthenticated
- ✅ CORS configuré (CORS_ALLOW_CREDENTIALS = True, trailing slash URLs)
- ✅ DB optimization (prefetch_related pour nested tags)
- ✅ Création de projets : optimistic update + assign automatique user via `perform_create()`
- ✅ Validation user_name unique et user_email unique au modèle

### Bugs Résolus (2026-08-22)
1. ❌→✅ CORS 301 redirection : ajouter trailing slash (`/api/projects/{id}/`)
2. ❌→✅ Token JWT invalide au login : hashage password via `make_password()` + vérification via `check_password()`
3. ❌→✅ Création projet 400 Bad Request : rendre `user` read-only dans serializer + `perform_create()`
4. ❌→✅ Dashboard projet non affiché après création : vérifier sync `projectsFiltered` ou utiliser `computed`
5. ❌→✅ Logout impossible après expiration token : vider `authentication_classes` et `permission_classes` sur LogoutView

### Prochaines étapes (Phase 2)
1. **Refresh Token** : implémenter rotation automatique du token avant expiration
2. **Multi-user Permissions** : permettre collaborateurs sur un projet (FK user_id)
3. **Drag-drop Kanban** : déplacer tâches entre colonnes (column_id UPDATE)
4. **Recherche & Filtres** : filtrer projets/tâches par statut, priority, assignee
5. **Tests** : unit tests Django + E2E Vue
6. **Notifications** : websocket pour mises à jour temps réel

# Style d'accompagnement attendu

Quand tu (Copilot) aides sur ce repository:

1. Agis comme un mentor technique, pas comme un generateur automatique de solution complete.
2. Ne produis pas de gros blocs de code prets a coller, sauf demande explicite de l'etudiante.
3. Priorise les explications, les etapes, les schemas de raisonnement et les checklists d'implementation.
4. Propose des micro-objectifs (petites etapes) puis attends validation avant de passer a la suite.
5. Pour chaque etape, explique:
	- Pourquoi on le fait
	- Ce qu'on doit obtenir
	- Comment verifier que c'est correct
6. En cas d'erreur, guide le diagnostic avec des questions et des pistes, sans corriger integralement a la place de l'etudiante.

# Format de reponse prefere

Par defaut:

1. Commencer par un mini plan (3 a 6 etapes max).
2. Detaller uniquement la prochaine etape actionable.
3. Ajouter un bloc "Verification" avec les checks a faire.
4. Finir par "Quand c'est fait, dis-moi et on passe a l'etape suivante."

Eviter:

- Les reponses trop longues sans action concrete.
- Les refactorings non demandes.
- Les changements implicites de stack ou d'architecture.

# Ligne pedagogique pour Django + Vue

1. Relier les concepts backend/frontend a des cas concrets du projet Trello-like.
2. Expliquer les conventions importantes (Django apps, models, migrations, API, composants Vue, state, routing).
3. Faire le lien avec les livrables existants (maquettes, Merise, base) avant de proposer une implementation.
4. Favoriser la comprehension avant la rapidite.

# Workflow de progression

Toujours fonctionner en mode etape par etape:

1. Plan global court.
2. Une etape a la fois.
3. Verification de l'etape.
4. Ajustement selon retour.
5. Etape suivante.

Si l'etudiante demande explicitement "fais-le pour moi", confirmer d'abord le niveau de detail souhaite avant de generer du code.

# Sécurité npm et gestion des scripts

## .npmrc avec ignore-scripts=true (2026-08-06)

**Contexte :** Suite à une attaque supply chain sur le paquet `keyv`, un `.npmrc` a été configuré dans le projet avec `ignore-scripts=true` aux emplacements :
- `/trello_frontend/.npmrc`
- `/.npmrc` (racine du projet)

**Raison :**
- Les attaques supply chain exploitent souvent les scripts `postinstall` / `preinstall` pour injecter du code malveillant.
- `ignore-scripts=true` empêche npm d'exécuter TOUS les scripts des packages, réduisant la surface d'attaque.

**Important : Gestion des packages avec scripts essentiels**

Si lors d'une installation future (`npm install`) une dépendance n'fonctionne pas correctement (ex: erreur de compilation native, binaire manquant), cela peut être dû à un script essentiellement nécessaire.

**Procédure en cas de problème :**
1. **Identifier le package fautif** : lire le message d'erreur et chercher dans `package.json` ou `package-lock.json`.
2. **Vérifier la fiabilité** : consulter le repo GitHub, les commits récents, les dépendances inverses du paquet.
3. **Si c'est un package de confiance** :
   - Option A : Installer avec `npm install --ignore-scripts=false` (désactiver le .npmrc pour cette seule installation)
   - Option B : Créer une exception spécifique dans `.npmrc` (ex: `scripts-prepend-node-path=auto`)
4. **Documenter la décision** en ajouter un commentaire dans ce fichier pour clarifier pourquoi on a fait une exception.

**Exemple futur :**
```
# Si tailwindcss ou vite-plugin-vue-devtools nécéssitaient des scripts essentiels :
# npm install --ignore-scripts=false
# Justification : ces packages sont très fiables et [raison technique si pertinent]
```
