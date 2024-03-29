from flask import request
from flask_restful import reqparse, Resource
from app.helpers.job_helpers import valid_json, scheduleJob, instance_by_name, get_scheduler, deleteJob
import json, boto3


ec2 = boto3.client('ec2', region_name='us-west-2')
parser = reqparse.RequestParser()
parser.add_argument('mock', type=bool, location='headers')
parser.add_argument('body', type=list, location='json')


class Job(Resource):
    def __init__(self, logging, job_name):

        self.logging = logging
        self.job_name = job_name
        self.scheduler = get_scheduler(self)

    # this method returns a single job description
    # It will return two type of jobs:
    #        - jobs that are scheduled but not started yet
    #        - jobs that are already started

    def get(self):

        if (self.job_name in [job.id for job in self.scheduler.get_jobs()]):
            # to extract proper job info from the scheduler
            scheduled = str(self.scheduler.get_job(self.job_name).trigger)
            time_str = scheduled.replace('date[', '').replace(']', '').replace(' UTC', '')
            image_name = self.scheduler.get_job(self.job_name).args[1]["image"]
            response_json = {
                "image": str(image_name),
                "time_scheduled": time_str,
                "status": "scheduled"
            }
            self.logging.info("Method: GET - {} - code: {}".format(self.job_name, 200))
            return response_json, 200
        else:
            return_data = instance_by_name(self.job_name)
            # check if there's any jobs running in aws
            if (return_data is not ""):
                self.logging.info("Method: GET - {} - code: {}".format(self.job_name, 200))
                return return_data, 200
            self.logging.info("Method: GET - {} - code: {}".format(self.job_name, 200))
            return json.loads('{"error": "Job name does not exists"}'), 400

    def delete(self):
        args = parser.parse_args()
        # check if job_name is scheduled
        if (self.job_name in [job.id for job in self.scheduler.get_jobs()]):
            self.scheduler.remove_job(self.job_name)
            self.logging.info("Method: DELETE - {} - code: {}".format(self.job_name, 200))
            return json.loads('{"message": "removed a scheduled job"}'), 200
        else:
            if (args["mock"]):
                self.logging.info("Method: Mock DELETE - {} - code: {}".format(self.job_name, 400))
                return json.loads('{"error": "job not found"}'), 400

        if (deleteJob(self)):
            self.logging.info("Method: DELETE - {} - code: {}".format(self.job_name, 200))
            return json.loads('{"message": "removed a running job"}'), 200
        self.logging.info("Method: DELETE - {} - code: {}".format(self.job_name, 400))
        return json.loads('{"error": "job not found"}'), 400

    def post(self):
        args = parser.parse_args()
        json_data = request.get_json()

        # make sure json is valid
        if (not valid_json(json_data)):
            return json.loads('{"error": "please provide a valid job"}'), 400

        # make sure the isn't already running
        if (instance_by_name(self.job_name) is not ""):
            return json.loads('{"error": "job name already running"}'), 409

        # make sure job isn't already scheduled
        if (self.job_name in [job.id for job in self.scheduler.get_jobs()]):
            return json.loads('{"error": "job already scheduled to run"}'), 409

        # schedule the job
        return scheduleJob(self, self.job_name, json_data, args["mock"])
