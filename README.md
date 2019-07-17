# Welcome To Schedular API 
> Built with flask app 

## API endpoints: 

## `/jobs` 
***
GET - desplays all the current jobs 

* Body: None

* response: 
```json 
[
    {
    "name": "job name",
    "time_scheduled": "date time",
    "status": "running/scheduled/done"
    }, 
    ...
]
```

## `/jobs/<name>`
***
GET - gets information about the specific job name

* Body: None

* response: 
```json
{
    "id": "id",
    "name": "job name",
    "time_scheduled": "date time",
    "status": "running/scheduled/done"
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
    "time_scheduled": "date time set to run",
    "status": "running/scheduled/done"
}
```

* response:
```
201 (sucess created) And {"message": "sucessfully added a job"} Or
400 (bad request)
```
