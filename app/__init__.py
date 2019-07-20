from flask import Flask
from flask_restful import Resource, Api
from app.classes.index import Index
from app.classes.job import Job
from app.classes.jobs import Jobs
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy
# from flask_apscheduler import APScheduler
# from app.classes.job import Job
# from app.job import get_job, post_job, delete_job, list_jobs

engine = sqlalchemy.create_engine('sqlite:///{}'.format('example.sqlite'))
scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', engine=engine)
scheduler.start()

# 2019-07-19 23:18:00.00
# scheduler = APScheduler()
# scheduler.init_app(app_instance)
# , resource_class_kwargs={'scheduler': scheduler}

app_instance = Flask(__name__)
api = Api(app_instance)

def configure_routes(api, scheduler):
    api.add_resource(Index, '/', '/index')
    api.add_resource(Job, 
        '/jobs/<job_name>', 
        '/jobs/<job_name>/', resource_class_kwargs={'scheduler': scheduler})
    api.add_resource(Jobs, 
        '/jobs', 
        '/jobs/', resource_class_kwargs={'scheduler': scheduler})
