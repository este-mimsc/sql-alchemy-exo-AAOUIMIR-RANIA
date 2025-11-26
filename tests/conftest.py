import sys
from pathlib import Path

import pytest

# Assure que la racine du projet est dans le path pour les imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app import create_app, db  # noqa: E402


@pytest.fixture()
def app():
    """Fixture pour créer l'application Flask en mode test."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # DB en mémoire pour tests
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    # Créer la base dans le contexte de l'app
    with app.app_context():
        db.create_all()
        yield app  # Move yield inside app_context

    # Nettoyage après les tests
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Fixture pour le client de test Flask."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Fixture pour runner CLI Flask (flask cli commands)."""
    return app.test_cli_runner()
