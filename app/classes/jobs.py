from flask import jsonify, request
from flask_restful import reqparse, Resource, reqparse
from app.helpers.job_helpers import instance_by_name

parser = reqparse.RequestParser()
parser.add_argument('mock', type=bool, location='headers')


class Jobs(Resource):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    # this method get all running aws jobs (instances) and scheduled jobs
    def get(self):
        return_json = {}
        for job in self.scheduler.get_jobs():
            return_json[job.id] = self.scheduler.get_job(job.id).args[1]
        running_instances = instance_by_name("", True)
        return {**return_json, **running_instances}, 200 