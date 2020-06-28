from flask import Flask
from flask_restful import Api

from COVIDMonitor.HomePage import HomePage
from COVIDMonitor.Query import Query
from COVIDMonitor.SearchPage import SearchPage
from COVIDMonitor.UploadPage import UploadPage
from COVIDMonitor.Uploader import Uploader


def create_app():
    app = Flask(__name__)
    api = Api(app)
    add_routes(api)
    return app


def add_routes(api):
    api.add_resource(HomePage, '/')
    api.add_resource(UploadPage, '/upload')
    api.add_resource(Uploader, '/uploader')
    api.add_resource(SearchPage, '/search')
    api.add_resource(Query, '/query')
