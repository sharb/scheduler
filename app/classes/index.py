import os, markdown2, sys
from flask_restful import Resource
from flask import make_response


class Index(Resource):
    def get(self):
        # os.path.dirname(root_path)
        with open( '/usr/src/app' + '/README.md', 'r') as readme_file:
            # read from readme
            readme_txt = readme_file.read()

            # return in HTML 
            html = markdown2.Markdown().convert(readme_txt)
            return make_response(html,200,{'Content-Type': 'text/html'})

