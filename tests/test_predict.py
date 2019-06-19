import os
import pytest
import sys
from werkzeug.test import EnvironBuilder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","app")))
from app import app
from utils import create_directory


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
    from views.save_image import ImageSaver
    from flask import Response
    def mock_save_image(self, image, token, label=""):
        return Response("Created", status=201)
    monkeypatch.setattr(ImageSaver,'save_image', mock_save_image)
    def mock_delete_image(self, path):
        return None
    monkeypatch.setattr(ImageSaver,'delete_image', mock_delete_image)

@pytest.fixture()
def patch_model(monkeypatch):
    from views.model import Model
    from flask import Response
    def mock_process_image(self, path):
        return path
    monkeypatch.setattr(Model,'process_image', mock_process_image)
    def mock_predict_classes(self, img):
        return 1, 1
    monkeypatch.setattr(Model,'predict_classes', mock_predict_classes)


def test_empty_query(client):
    response = client.post('/api/predict', data={})
    assert response.status_code == 400

def test_query_no_image(client):
    response = client.post('/api/predict', data={
        "token": "token"
    })
    assert response.status_code == 400

def test_complete_query(client, patch_image_saver, patch_model):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/predict',
            method='POST',
            content_type='multipart/form-data',
            data={
                "token": "token"
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 201

def test_query_no_token(client):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/predict',
            method='POST',
            content_type='multipart/form-data',
            data={
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400

def test_empty_token(client):
    with open(os.path.join(os.path.dirname(__file__), "polito.jpeg"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/predict',
            method='POST',
            content_type='multipart/form-data',
            data={
                "token": ""
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400

def test_other_extension(client):
    with open(os.path.join(os.path.dirname(__file__), "random.txt"), 'rb') as img:
        query = EnvironBuilder(
            path='/api/predict',
            method='POST',
            content_type='multipart/form-data',
            data={
                "token": "secret"
            }
        )
        query.files.add_file(name='image',file=img)
        response = client.open(query)
        assert response.status_code == 400