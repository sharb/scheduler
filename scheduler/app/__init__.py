
from flask import Flask, request
from app.classes.index import Index
from app.classes.job import Job
from app.classes.jobs import Jobs
import logging

# start the app
app = Flask(__name__)

# configure logging
logging.basicConfig(filename='file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# configure routes
@app.route("/")
@app.route("/index")
def index():
    index = Index()
    return index.get()


@app.route('/jobs/<job_name>', methods=['GET', 'POST', 'DELETE'])
@app.route('/jobs/<job_name>/', methods=['GET', 'POST', 'DELETE'])
def job(job_name):
    # initialize Job class
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
    # initialize Jobs class
    jobs = Jobs(logging)
    if request.method == 'GET':
        return jobs.get()

    if request.method == 'DELETE':
        return jobs.delete()
