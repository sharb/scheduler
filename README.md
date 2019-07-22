# Welcome To Schedular API 
> Built with flask app 

## API endpoints: 

## `/jobs` 
***
GET - desplays all the current jobs 

* Body: None

* response: 
```json 
{
    "some-job": {
        "image": "nginx",
        "time_scheduled": "2019-07-23 08:30:00.00",
    },
    "other-job": {
        "image": "nginx",
        "time_scheduled": "2019-07-24 08:30:00.00",
    },
    "yes-another": {
        "dns_name": "ec2-34-222-141-76.us-west-2.compute.amazonaws.com",
        "instance_id": "i-01c5128562d5f93da",
        "status": "running"
    }
}
```

## `/jobs/<name>`
***
GET - gets information about the specific job name

* Body: None

* response (if the job hasn't run): 
```json
{
    "name": "job name",
    "time_scheduled": "date time",
}
```
* response (if the job already ran): 
```json
{
    "dns_name": "ec2-34-222-141-76.us-west-2.compute.amazonaws.com",
    "instance_id": "i-01c5128562d5f93da",
    "status": "running"
}
```

DELETE - deletes a specific job with name 

* Body: None

* Response: 
```
204 (success but no content) Or
404 (not found)
```

POST - adds a job 

* Body: 
```json
{
    "name": "job name",
    "time_scheduled": "date time set to run"
}
```

* response:
```
201 (sucess created) And {"message": "sucessfully added a job"} Or
400 (bad request)
```
