from flask import Flask
from flask_restful import Resource, Api
from app.classes.index import Index
from app.classes.job import Job
# from app.classes.job import Job
# from app.job import get_job, post_job, delete_job, list_jobs

jobs = {}

app_instance = Flask(__name__)
api = Api(app_instance)

def configure_routes(api):
    api.add_resource(Index, '/', '/index')
    api.add_resource(Job, '/jobs/<job_name>')
