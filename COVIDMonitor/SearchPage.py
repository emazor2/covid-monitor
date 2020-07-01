from flask import make_response, render_template
from flask_restful import Resource


class SearchPage(Resource):
    def get(self):
        """Displays the search page."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('search.html'), 200, headers)
