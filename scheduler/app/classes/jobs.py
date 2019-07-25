from flask import jsonify, request
from flask_restful import reqparse, Resource, reqparse
from app.helpers.job_helpers import instance_by_name, get_scheduler
import boto3, json

ec2 = boto3.client('ec2', region_name='us-west-2')
parser = reqparse.RequestParser()
parser.add_argument('mock', type=bool, location='headers')


class Jobs(Resource):
    def __init__(self, logging):
        self.logging = logging
        self.scheduler = get_scheduler(self)

    # this method get all running aws jobs (instances) and scheduled jobs
    def get(self):
        return_json = {}
        for job in self.scheduler.get_jobs():
            return_json[job.id] = self.scheduler.get_job(job.id).args[1]
            return_json[job.id]["status"] = "scheduled"
        # the second parameter means: get all instances from aws that are running
        running_instances = instance_by_name("", True)
        self.logging.info("Method: GET - All JObs - code: {}".format(200))
        return {**return_json, **running_instances}, 200 

    def delete(self):
        args = parser.parse_args()
        # remove all jobs in the scheduler
        [self.scheduler.remove_job(job.id) for job in self.scheduler.get_jobs()]

        # remove all jobs in ec2 instance if the header is not mocked
        if (not args["mock"]):
            running_instances = instance_by_name("", True)
            for job_name, job_data in running_instances.items():
                    response = ec2.terminate_instances(
                        InstanceIds=[job_data['instance_id'],]
                    )
        else:
            self.logging.info("Method: DELETE - Mock Deleted All Jobs - code: {}".format(200))  

        self.logging.info("Method: DELETE - Deleted All Jobs - code: {}".format(200))  
        return json.loads('{"message": "all job removed"}'), 200


