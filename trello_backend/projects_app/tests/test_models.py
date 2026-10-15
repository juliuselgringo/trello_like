# projects_app/tests/test_models.py
from django.test import TestCase
from django.db import connection
from projects_app.models import Project, User
from datetime import date

class ProjectModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Crée les tables manuellement AVANT les tests (car managed=False)."""
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(User)
            schema_editor.create_model(Project)

    def setUp(self):
        """Crée un utilisateur pour chaque test."""
        self.user = User.objects.create(
            user_name="testuser",
            user_email="test@example.com",
            user_password="testpass123"
        )

    def test_project_creation(self):
        project = Project.objects.create(
            project_name="Mon premier projet",
            user=self.user,
            project_description="Description test",
            project_creation_date=date(2024, 1, 1),
        )
        self.assertEqual(project.project_name, "Mon premier projet")

    def test_project_name_required(self):
        """Test que project_name est obligatoire."""
        project = Project(
            user=self.user,
            project_creation_date=date(2024, 1, 1),
            project_description="Sans nom",
            # project_name manquant
        )
        with self.assertRaises(Exception):
            project.full_clean()  # ← Force la validation des champs

    def test_project_str_method(self):
        project = Project.objects.create(
            project_name="Projet test",
            user=self.user,
            project_creation_date=date(2024, 1, 1),
        )
        self.assertEqual(str(project), "Projet test")