import io

from app.models import LogFile
from app import db


def test_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_upload_page(client):
    response = client.get("/logs/upload")
    assert response.status_code == 200
    assert b"Upload" in response.data


def test_logs_list_page(client):
    response = client.get("/logs/")
    assert response.status_code == 200


def test_upload_valid_file(client, sample_log_content):
    data = {
        "file": (io.BytesIO(sample_log_content.encode()), "test.log"),
    }
    response = client.post(
        "/logs/upload", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 302


def test_upload_invalid_extension(client):
    data = {
        "file": (io.BytesIO(b"some content"), "test.pdf"),
    }
    response = client.post(
        "/logs/upload", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200


def test_view_log_detail(client, app, sample_log_content):
    data = {
        "file": (io.BytesIO(sample_log_content.encode()), "detail_test.log"),
    }
    client.post("/logs/upload", data=data, content_type="multipart/form-data")

    with app.app_context():
        log_file = LogFile.query.first()
        file_id = log_file.id

    response = client.get(f"/logs/{file_id}")
    assert response.status_code == 200
    assert b"detail_test.log" in response.data


def test_delete_log(client, app, sample_log_content):
    data = {
        "file": (io.BytesIO(sample_log_content.encode()), "delete_test.log"),
    }
    client.post("/logs/upload", data=data, content_type="multipart/form-data")

    with app.app_context():
        log_file = LogFile.query.first()
        file_id = log_file.id

    response = client.post(f"/logs/{file_id}/delete", follow_redirects=True)
    assert response.status_code == 200


def test_404_page(client):
    response = client.get("/nonexistent-page")
    assert response.status_code == 404


def test_search_by_filename(client, app, sample_log_content):
    data = {
        "file": (io.BytesIO(sample_log_content.encode()), "searchable.log"),
    }
    client.post("/logs/upload", data=data, content_type="multipart/form-data")
    response = client.get("/logs/?filename=searchable")
    assert response.status_code == 200
    assert b"searchable.log" in response.data


def test_filter_by_level(client, app, sample_log_content):
    data = {
        "file": (io.BytesIO(sample_log_content.encode()), "filter_test.log"),
    }
    client.post("/logs/upload", data=data, content_type="multipart/form-data")

    with app.app_context():
        log_file = LogFile.query.first()
        file_id = log_file.id

    response = client.get(f"/logs/{file_id}?level=ERROR")
    assert response.status_code == 200
