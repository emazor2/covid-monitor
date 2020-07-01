from flask import make_response, render_template
from flask_restful import Resource


class UploadPage(Resource):
    def get(self):
        """Displays the upload page."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('upload.html'), 200, headers)
