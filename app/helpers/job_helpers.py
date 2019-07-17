import os 

def store_job(job_name, json_data):
    jobs = {}
    if (os.path.isfile("jobs.txt")):
        with open('jobs.txt','r') as f:
            jobs = eval(f.read())

    jobs[job_name] = json_data
    with open('jobs.txt','w') as f:
        f.write(str(jobs))

    # print("printing all jobs ---", file=sys.stdout)
    # print(jobs, file=sys.stdout)

    return jobs
    

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

def already_exists(job_name, DummyData):
    jobs = {}
    if (os.path.isfile("jobs.txt")):
        with open('jobs.txt','r') as f:
            jobs = eval(f.read())
        if (job_name in jobs):
            return True
        else:
            return False
    else: 
        return False
