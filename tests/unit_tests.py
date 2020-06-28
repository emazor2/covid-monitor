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


def test_query_json():
    data = {"query_type": "test",
            "key_type": "countries",
            "key_list": "Angola",
            "date_start": "2020-06-15",
            "date_end": "2020-06-15",
            "return_format": "json"}
    expected = [
        {'Province_State': '', 'Country_Region': 'Angola', 'Combined_Key': '', 'Lat': '-11.2027', 'Long_': '17.8739',
         '2020-06-15': '142'}]
    json_file = pd.DataFrame(expected).to_json(orient="records")

    response = app.test_client().post('/query', data=data, follow_redirects=True, content_type='multipart/form-data')
    assert json_file == response.data.decode("utf-8")
    assert response.status_code == 200


def test_query_csv():
    data = {"query_type": "test",
            "key_type": "countries",
            "key_list": "Angola",
            "date_start": "2020-06-15",
            "date_end": "2020-06-15",
            "return_format": "csv"}
    expected = [
        {'Province_State': '', 'Country_Region': 'Angola', 'Combined_Key': '', 'Lat': '-11.2027', 'Long_': '17.8739',
         '2020-06-15': '142'}]
    csv_file = pd.DataFrame(expected).to_csv()

    response = app.test_client().post('/query', data=data, follow_redirects=True, content_type='multipart/form-data')
    assert csv_file == response.data.decode("utf-8")
    assert response.status_code == 200


def test_query_html():
    data = {"query_type": "test",
            "key_type": "countries",
            "key_list": "Angola",
            "date_start": "2020-06-15",
            "date_end": "2020-06-15",
            "return_format": "text"}
    expected = [
        {'Province_State': '', 'Country_Region': 'Angola', 'Combined_Key': '', 'Lat': '-11.2027', 'Long_': '17.8739',
         '2020-06-15': '142'}]
    html_file = pd.DataFrame(expected).to_html()

    response = app.test_client().post('/query', data=data, follow_redirects=True, content_type='multipart/form-data')
    assert html_file == response.data.decode("utf-8")
    assert response.status_code == 200


def test_query_line_plot():
    data = {"query_type": "test",
            "key_type": "countries",
            "key_list": "Angola",
            "date_start": "2020-06-15",
            "date_end": "2020-06-15",
            "return_format": "line_plot"}
    response = app.test_client().post('/query', data=data, follow_redirects=True, content_type='multipart/form-data')
    assert response.status_code == 200
