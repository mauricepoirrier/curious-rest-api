import os
import tempfile
import pytest
import sys
from werkzeug.test import EnvironBuilder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.app import app
from app.utils import create_directory


@pytest.fixture
def client():
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_DIRECTORY', 'app/persistent/')
    create_directory(app.config['UPLOAD_FOLDER'])
    app.config['TESTING'] = True
    client = app.test_client()
    return client

@pytest.fixture(autouse=True)
def delete_file():
    yield
    upload_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'app',\
         'persistent'))
    for root, dirs, files in os.walk(upload_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

@pytest.fixture()
def patch_image_saver(monkeypatch):
    from app.views.save_image import ImageSaver
    from flask import Response
    def mock_save_image(self, image, token, label=""):
        return Response("Created", status=201)
    monkeypatch.setattr(ImageSaver, 'save_image', mock_save_image)

def test_get_root(client):
    ''' Getting root '''
    response = client.get('/')
    assert response.status_code == 404

def test_empty_query(client):
    response = client.post('/api/upload', data={})
    assert response.status_code == 400

def test_query_no_image(client):
    response = client.post('/api/upload', data={
        "label": "abc",
        "token": "token"
    })
    assert response.status_code == 400

def test_complete_query(client, patch_image_saver):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/upload',
            method='POST',
            content_type='multipart/form-data',
            data={
                "label": "dog",
                "token": "token"
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 201

def test_query_no_label(client):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/upload',
            method='POST',
            content_type='multipart/form-data',
            data={
                "token": "token"
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400

def test_query_no_token(client):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/upload',
            method='POST',
            content_type='multipart/form-data',
            data={
                "label": "dog"
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400

def test_empty_token(client):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/upload',
            method='POST',
            content_type='multipart/form-data',
            data={
                "label": "dog",
                "token": ""
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400
