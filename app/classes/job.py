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

    def get(self, job_name):
        if (job_name in [job.id for job in self.scheduler.get_jobs()]):
            scheduled = self.scheduler.get_job(job_name).trigger
            image_name = self.scheduler.get_job(job_name).args[1]["image"]
            response_json = {
                "image": str(image_name),
                "time_scheduled": str(scheduled)
            }
            # print("############ scheduled at:  " + str(image_name))
            return response_json, 200
        else:
            return_data = instance_by_name(job_name)
            if (return_data is not ""):
                return return_data, 200
            return json.loads('{"error": "did not find job"}'), 400

    def delete(self, job_name):
        # abort_if_todo_doesnt_exist(todo_id)
        del jobs[job_name]
        return job, 204

    def post(self, job_name):
        args = parser.parse_args()
        json_data = request.get_json()

        # provide checks bofore scheduling the job
        if (not valid_json(json_data)):
            return json.loads('{"error": "please provide a valid job"}'), 400
        
        if (instance_by_name(job_name) is not ""):
            return json.loads('{"error": "job name already running"}'), 409
        
        if (job_name in [job.id for job in self.scheduler.get_jobs()]):
            return json.loads('{"error": "job already scheduled to run"}'), 409

        # schedule the job
        return scheduleJob(self, job_name, json_data, args["mock"])
        