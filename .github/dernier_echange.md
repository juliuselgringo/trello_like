tu as des infos dans .github/instructions.md. Je veux pour l'instant 2, 3 endpoints afin de vérifier que tout fonctionne correctement et pour apprendre pas à pas. Peut être juste l'endpoint qui permet de requêter le project?














Perfect ! Voici le plan pour créer votre premier endpoint fonctionnel :

Mini-plan : Endpoint GET /projects
Installer Django REST Framework (dépendance externe)
Créer un serializer pour Project (transformation modèle → JSON)
Créer une viewset pour servir les projets (logique API)
Configurer les URLs (router + endpoints)
Tester l'endpoint (vérifier que ça répond)
Étape 1️⃣ : Installer Django REST Framework
Pourquoi : DRF simplifie la création d'API REST (serializers, viewsets, authentification, pagination, etc.)

Ce que vous devez faire :

Dans le terminal, assurez-vous que votre venv est activé
Exécutez : pip install djangorestframework
Ajoutez 'rest_framework' dans INSTALLED_APPS dans backDjango/settings.py (après les apps Django officielles, avant projects_app)
Vérification :

Lancez python manage.py check
Vous ne devez pas voir d'erreurs concernant rest_framework
Quand c'est fait, dis-moi et on passe à l'étape 2 (créer le serializer).