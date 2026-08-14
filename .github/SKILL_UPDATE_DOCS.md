# Skill: Mettre à jour la documentation du Trello-like

## 📌 Usage

**Appel** : `@copilot /update-trello-docs`

**Description** : Met à jour la documentation du projet (README et copilot-instructions) après une session de développement.

---

## 📋 Ce qu'on met à jour

### 1. **README.md** (racine)
- Vue globale du projet
- État Frontend / Backend
- Prochaines étapes

### 2. **trello_backend/README.md**
- Endpoints API (authentification + CRUD)
- Setup instructions
- Configuration CORS + JWT

### 3. **trello_frontend/README.md**
- Authentification (credentials: 'include')
- Endpoints utilisés
- Setup et démarrage dev

### 4. **.github/copilot-instructions.md**
- État actuel du projet (date)
- Statut Frontend (✅/🔄/⏳)
- Statut Backend (✅/🔄/⏳)
- Prochaines étapes

---

## 🎯 Checklist de mise à jour

### Avant de mettre à jour, demander à l'utilisateur :

- [ ] Quelle feature a été complétée ? (JWT, drag-drop, etc.)
- [ ] État Frontend : ✅ complété / 🔄 en cours / ⏳ à faire
- [ ] État Backend : ✅ complété / 🔄 en cours / ⏳ à faire
- [ ] Nouveaux endpoints ? (si oui, documenter avec exemples curl)

### Mise à jour des fichiers :

1. [ ] README.md racine : mettre à jour sections "État du projet"
2. [ ] trello_backend/README.md : ajouter nouveaux endpoints si applicable
3. [ ] trello_frontend/README.md : ajouter nouveaux points d'intégration
4. [ ] copilot-instructions.md : mettre à jour date + listes de statuts

---

## 📝 Template pour l'état

```markdown
## État du projet (YYYY-MM-DD)

### Frontend ✅/🔄/⏳
- Feature 1: description courte
- Feature 2: description courte

### Backend ✅/🔄/⏳
- Feature 1: description courte
- Feature 2: description courte

### Prochaines étapes
1. Étape suivante
2. Étape suivante
```

---

## 🔑 Points clés à documenter

### Si JWT/Auth :
- HttpOnly cookies
- SameSite=Lax
- CORS_ALLOW_CREDENTIALS = True
- Endpoints : /api/auth/login/, /api/auth/register/

### Si nouveaux endpoints :
- Incluire exemples curl
- Mentionner la permission (IsAuthenticated, etc.)
- Paramètres de requête (project_id, etc.)

### Si responsive/UI :
- Breakpoints (mobile, tablet, desktop)
- Framework utilisé (Flexbox, Grid)

---

## ⚡ Rappel pédagogique

- Garder le ton **pédagogique** dans copilot-instructions.md
- Mettre "pourquoi" et "comment", pas juste "quoi"
- Documenter les décisions (ex: pourquoi JWT vs sessions)

