from COVIDMonitor.main import app
from flask import render_template
import pandas as pd


def test_home():
    response = app.test_client().get('/')
    with app.app_context():
        expected = render_template('home.html')
    assert response.data.decode("utf-8") == expected


def test_upload():
    response = app.test_client().get('/upload')
    with app.app_context():
        expected = render_template('upload.html')
    assert response.data.decode("utf-8") == expected
    assert response.status_code == 200


def test_search():
    response = app.test_client().get('/search')
    with app.app_context():
        expected = render_template('search.html')
    assert response.data.decode("utf-8") == expected
    assert response.status_code == 200


def test_uploader():
    file = open('COVIDMonitor/test_file.csv', "rb")
    data = {"file": file, "file_type": "time", "data_type": "test"}
    response = app.test_client().post('/uploader', data=data, follow_redirects=True, content_type='multipart/form-data')
    with app.app_context():
        home_data = render_template('home.html')
    assert response.data.decode("utf-8") == home_data
    assert response.status_code == 200
