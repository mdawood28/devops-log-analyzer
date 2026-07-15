import os

import pytest

from app import create_app, db as _db


@pytest.fixture
def app(tmp_path):
    app = create_app("testing")
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        }
    )

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def sample_log_content():
    return (
        "2024-01-15 10:30:00 INFO Application started\n"
        "2024-01-15 10:30:05 WARNING Disk usage at 85%\n"
        "2024-01-15 10:30:10 ERROR Database connection failed\n"
        "2024-01-15 10:31:00 DEBUG Cache cleared\n"
        "2024-01-15 10:32:00 CRITICAL System overload detected\n"
    )
