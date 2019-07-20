from flask import jsonify, request
from flask_restful import reqparse, Resource, reqparse
from app.helpers.job_helpers import valid_json, scheduleJob, instance_by_name
import json, sys, os, datetime


parser = reqparse.RequestParser()
parser.add_argument('mock', type=bool, location='headers')
parser.add_argument('body', type=list, location='json')


class Job(Resource):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    # this method gets a single job description
    # It will get two type of jobs:
    #        - jobs that are scheduled but not started yet
    #        - jobs that are already started 
    def get(self, job_name):
        if (job_name in [job.id for job in self.scheduler.get_jobs()]):
            # to extract proper job info from the scheduler
            scheduled = str(self.scheduler.get_job(job_name).trigger)
            time_str = scheduled.replace('date[', '').replace(']', '').replace(' UTC', '')
            image_name = self.scheduler.get_job(job_name).args[1]["image"]
            response_json = {
                "image": str(image_name),
                "time_scheduled": time_str
            }
            return response_json, 200
        else:
            return_data = instance_by_name(job_name)
            # check if there's any jobs running in aws 
            if (return_data is not ""):
                return return_data, 200
            return json.loads('{"error": "Job name does not exists"}'), 400

    def delete(self, job_name):
        # abort_if_todo_doesnt_exist(todo_id)
        del jobs[job_name]
        return job, 204

    def post(self, job_name):
        args = parser.parse_args()
        json_data = request.get_json()

        # make sure json is valid
        if (not valid_json(json_data)):
            return json.loads('{"error": "please provide a valid job"}'), 400
        
        # make sure the isn't already running 
        if (instance_by_name(job_name) is not ""):
            return json.loads('{"error": "job name already running"}'), 409
        
        # make sure job isn't already scheduled
        if (job_name in [job.id for job in self.scheduler.get_jobs()]):
            return json.loads('{"error": "job already scheduled to run"}'), 409

        # schedule the job
        return scheduleJob(self, job_name, json_data, args["mock"])
        