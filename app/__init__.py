from flask import Flask
from flask_restful import Resource, Api
from app.classes.index import Index
from app.classes.job import Job
from app.classes.jobs import Jobs
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy, logging
from logging.handlers import RotatingFileHandler

engine = sqlalchemy.create_engine('sqlite:///{}'.format('example.sqlite'))
scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', engine=engine)
scheduler.start()

app_instance = Flask(__name__)
api = Api(app_instance)

logging.basicConfig(filename='file.log',level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def configure_routes(api, scheduler, logging):
    logging.info("configuring routes")
    api.add_resource(Index, '/', '/index')
    api.add_resource(Job, 
        '/jobs/<job_name>', 
        '/jobs/<job_name>/', resource_class_kwargs={'scheduler': scheduler, 'logging': logging})
    api.add_resource(Jobs, 
        '/jobs', 
        '/jobs/', resource_class_kwargs={'scheduler': scheduler, 'logging': logging})

