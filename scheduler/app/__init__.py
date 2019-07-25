
from flask import Flask, escape, request
from flask_restful import Resource, Api
from app.classes.index import Index
from app.classes.job import Job
from app.classes.jobs import Jobs
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy, logging

# # this creates the sqlalchemy database engine for the scheduler
# engine = sqlalchemy.create_engine('sqlite:///{}'.format('database.sqlite'))
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore('sqlalchemy', engine=engine)
# scheduler.start()

# start the app
app = Flask(__name__)
# api = Api(app)

# configure logging
logging.basicConfig(filename='file.log',level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# configure routes
# def configure_routes(api, scheduler, logging):
def configure_routes(api):
    # logging.info("HEYYYYYYY")
    # logging.info("configuring routes")
    api.add_resource(Index, '/', '/index')
    # api.add_resource(Job, 
    #     '/jobs/<job_name>', 
    #     '/jobs/<job_name>/', resource_class_kwargs={'scheduler': scheduler, 'logging': logging})
    # api.add_resource(Jobs, 
    #     '/jobs', 
    #     '/jobs/', resource_class_kwargs={'scheduler': scheduler, 'logging': logging})

@app.route("/")
@app.route("/index")
def index():
    index = Index()
    return index.get()

@app.route('/jobs/<job_name>', methods=['GET', 'POST', 'DELETE'])
@app.route('/jobs/<job_name>/', methods=['GET', 'POST', 'DELETE'])
def job(job_name):
    job = Job(logging, job_name)
    if request.method == 'GET':
        return job.get()

    if request.method == 'POST':
        return job.post()

    if request.method == 'DELETE':
        return job.delete()

@app.route('/jobs', methods=['GET', 'DELETE'])
@app.route('/jobs/', methods=['GET', 'DELETE'])
def jobs():
    jobs = Jobs(logging)
    if request.method == 'GET':
        return jobs.get()

    if request.method == 'DELETE':
        return jobs.delete()