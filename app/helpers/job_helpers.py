import os, datetime, sys, json, boto3
from app.helpers.create_instance import create_instance

ec2 = boto3.client('ec2', region_name='us-west-2')

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
def instance_by_name(job_name):
    # return the matched instance details if the job name matches the "Name" tag in the instance 
    # and if it's not terminating
    custom_filter = [{'Name':'tag:Createdby',  'Values': ['Scheduler-Api']}]
    response = ec2.describe_instances(Filters=custom_filter)
    for instances in response["Reservations"]:
        # print("######## DEBUG ####################", file=sys.stdout)
        # print("jobname: " + job_name, file=sys.stdout)
        # look for the correct name of the tag 
        for tag in instances["Instances"][0]["Tags"]:
            if (tag['Key'] == "Name"):
                tagName = tag['Value']
        # print("Tag: " + tagName, file=sys.stdout)
        # print("status: " + instances["Instances"][0]['State']['Name'], file=sys.stdout)
        # print("is it terminated? :" + str(instances["Instances"][0]['State']['Name'] in ['shutting-down', 'terminated', 'stopping', 'stopped']), file=sys.stdout)
        # print("######## DEBUG ####################", file=sys.stdout)
        if ((tagName == job_name) and 
                not (instances["Instances"][0]['State']['Name'] in 
                ['shutting-down', 'terminated', 'stopping', 'stopped']) ):
            # print("######## INSIDE THE IF ####################", file=sys.stdout)
            return_data = {
                "dnsName": instances["Instances"][0]["PublicDnsName"],
                "id": instances["Instances"][0]["InstanceId"],
                "status": instances["Instances"][0]['State']['Name']
            }
            print("############### return found instanse", file=sys.stdout)
            return return_data
    return ""
            

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
    print("before schedule ########################################  " + str(self.scheduler.get_jobs()), file=sys.stdout)
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

# [i-0d03ec1dee46e607e i-03788342c20bef5d2 i-01c27eb143ef6ece6]