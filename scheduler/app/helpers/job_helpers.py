import os, datetime, sys, json, boto3, sqlalchemy, psycopg2
from app.helpers.create_instance import create_instance
from apscheduler.schedulers.background import BackgroundScheduler


ec2 = boto3.client('ec2', region_name='us-west-2')

# this method will valied if certain keys in json exists 
# and it will validate all the values are of type str
def valid_json(json_data):
    if (json_data == None):
        return False
    if (("image" not in json_data) or 
            ("time_scheduled" not in json_data)):
        return False
    if((not isinstance(json_data["image"], str)) or
            (not isinstance(json_data["time_scheduled"], str))):
        return False
    return True
    
# this method will return the matched instance details if the job name matches the "Name" tag in the instance 
# only if it's not terminating
# if get_all_instances is true, just return all running or pending instances
def instance_by_name(job_name, get_all_instances=False):
    return_data = {}
    custom_filter = [{'Name':'tag:Createdby',  'Values': ['Scheduler-Api']}]
    response = ec2.describe_instances(Filters=custom_filter)
    for instances in response["Reservations"]:
        for tag in instances["Instances"][0]["Tags"]:
            if (tag['Key'] == "Name"):
                tagName = tag['Value']
        if (get_all_instances):
            if (not (instances["Instances"][0]['State']['Name'] in 
                ['shutting-down', 'terminated', 'stopping', 'stopped']) ):
                return_data[tagName] = {
                        "dns_name": instances["Instances"][0]["PublicDnsName"],
                        "instance_id": instances["Instances"][0]["InstanceId"],
                        "status": instances["Instances"][0]['State']['Name']
                }      
        else: 
            if ((tagName == job_name) and 
                    not (instances["Instances"][0]['State']['Name'] in 
                    ['shutting-down', 'terminated', 'stopping', 'stopped']) ):
                return_data = {
                    "dns_name": instances["Instances"][0]["PublicDnsName"],
                    "instance_id": instances["Instances"][0]["InstanceId"],
                    "status": instances["Instances"][0]['State']['Name']
                }
                return return_data
    if (get_all_instances):
        return return_data
    else:
        return ""
            
# this method will return if the given str is in a datetime format or not
def validTime(time_scheduled_str):
        now = datetime.datetime.now()
        try: 
            time_scheduled = datetime.datetime.strptime(time_scheduled_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return json.loads('{"error": "datetime format not valid"}'), False
        if(now > time_scheduled):
            return json.loads('{"error": "cannot schedule job in the past"}'), False

        return time_scheduled, True


# this method will schedule the given job at the appropriate time
# this will return the json message of when it was sheduled 
def scheduleJob(self, job_name, json_data, mock):
    if(not json_data["time_scheduled"] == "now"):
        time_scheduled, valid = validTime(json_data["time_scheduled"])
        if (not valid):
            self.logging.info("Method: POST - {} - code: {}".format(job_name, 400))
            return time_scheduled, 400

        # if json is valid, schedule the job
        self.scheduler.add_job(create_instance, trigger='date', run_date=time_scheduled, args=[job_name, json_data, mock], id=job_name)
        delta = (time_scheduled - datetime.datetime.now())
        self.logging.info("Method: POST - {} - code: {}".format(job_name, 201))
        return json.loads('{"message": "job scheduled in ' + str(delta) + '"}'), 201

    self.logging.info("Method: POST - {} - code: {}".format(job_name, 201))
    self.scheduler.add_job(create_instance, trigger='date', run_date=datetime.datetime.now(), args=[job_name, json_data, mock], id=job_name)
    if (mock):
        return json.loads('{"message": "job mock scheduled"}'), 201
    return json.loads('{"message": "job scheduled now"}'), 201 

# get's the scheduler in the Jobs/Job init() 
def get_scheduler(self):
    self.logging.info("Initialized scheduler and sqlalchemy")
    engine = sqlalchemy.create_engine(os.environ['SQLITE_DB'])
    scheduler = BackgroundScheduler()
    # this creates the sqlalchemy database engine for the scheduler
    scheduler.add_jobstore('sqlalchemy', engine=engine)
    scheduler.start()
    return scheduler
