from flask import jsonify, request
from flask_restful import reqparse, Resource, reqparse
from app.helpers.job_helpers import store_job, valid_json, already_exists
import json, sys, os

parser = reqparse.RequestParser()
parser.add_argument('DummyData', type=bool, location='headers')
parser.add_argument('body', type=list, location='json')

class Job(Resource):
    jobs = {}

    def get(self, job_name):
        args = parser.parse_args()
        if (args["DummyData"]):
            if (os.path.isfile("jobs.txt")):
                with open('jobs.txt','r') as f:
                    jobs = eval(f.read())
                
                print("job found!: +++ " + str(jobs[job_name]), file=sys.stdout)
                return json.loads(jobs[job_name]), 200
        return jobs, 200

    def delete(self, job_name):
        # abort_if_todo_doesnt_exist(todo_id)
        del jobs[job_name]
        return job, 204

    def post(self, job_name):
        args = parser.parse_args()
        json_data = request.get_json()

        if (not valid_json(json_data)):
            return json.loads('{"error": "please provide a valid job"}'), 400
        
        if (already_exists(job_name, args["DummyData"])):
            return json.loads('{"error": "this job name already exists"}'), 400

        

        if (args["DummyData"]):
            jobs = store_job(job_name, json_data)
            # return json.loads('{"message": "job added sucessfully"}'), 201
            return jobs, 201
            
        return args["DummyData"], 201


        