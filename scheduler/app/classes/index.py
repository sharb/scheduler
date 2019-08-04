import markdown2
from flask_restful import Resource
from flask import make_response


class Index(Resource):
    def get(self):
        with open('README.md', 'r') as readme_file:
            readme_txt = readme_file.read()
            # return in HTML
            html = markdown2.Markdown().convert(readme_txt)
            return make_response(html, 200, {'Content-Type': 'text/html'})
