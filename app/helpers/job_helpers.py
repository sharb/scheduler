import os, datetime, sys, json
from app.helpers.create_instance import create_instance

# def store_job(job_name, json_data):
#     jobs = {}
#     if (os.path.isfile("jobs.txt")):
#         with open('jobs.txt','r') as f:
#             jobs = eval(f.read())

#     jobs[job_name] = json_data
#     with open('jobs.txt','w') as f:
#         f.write(str(jobs))

#     # print("printing all jobs ---", file=sys.stdout)
#     # print(jobs, file=sys.stdout)

#     return jobs
    

def valid_json(json_data):
    if (("image" not in json_data) or 
            ("time_scheduled" not in json_data) or
            ("status" not in json_data)):
        return False
    if((not isinstance(json_data["image"], str)) or
            (not isinstance(json_data["time_scheduled"], str)) or
            (not isinstance(json_data["status"], str))):
        # print("inside validate data --- not a str ---", file=sys.stdout)
        return False

    return True

# def already_exists(job_name, DummyData):
#     jobs = {}
#     if(DummyData):
#         if (os.path.isfile("jobs.txt")):
#             with open('jobs.txt','r') as f:
#                 jobs = eval(f.read())
#             if (job_name in jobs):
#                 return True
#             else:
#                 return False
#         else: 
#             return False
#     else:
#         return False
def validTime(time_scheduled_str):
        now = datetime.datetime.now()
        try: 
            time_scheduled = datetime.datetime.strptime(time_scheduled_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return json.loads('{"error": "datetime format not valid"}'), False
        if(now > time_scheduled):
            return json.loads('{"error": "cannot schedule job in the past"}'), False

        return time_scheduled, True



def scheduleJob(self, job_name, json_data, mock):
    # 'sqlalchemy'
    # self.scheduler.remove_all_jobs()
    print("before schedule ########################################  " + str(self.scheduler.get_jobs()), file=sys.stdout)
    # check if job already exists in shceduler
    if (job_name in [job.id for job in self.scheduler.get_jobs()]):
        return json.loads('{"error": "job already exists"}'), 409

    if(not json_data["time_scheduled"] == "now"):
        time_scheduled, valid = validTime(json_data["time_scheduled"])
        if (not valid):
            return time_scheduled, 400

        # if json is valid, schedule the job
        self.scheduler.add_job(create_instance, trigger='date', run_date=time_scheduled, args=[job_name, json_data, mock], id=job_name)
        delta = (time_scheduled - datetime.datetime.now())
        return json.loads('{"message": "job scheduled in ' + str(delta) + '"}'), 201

    self.scheduler.add_job(create_instance, trigger='date', run_date=datetime.datetime.now(), args=[job_name, json_data, mock], id=job_name)
    return json.loads('{"message": "job scheduled now"}'), 201 

