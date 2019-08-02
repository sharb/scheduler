# Scheduler API

This api is used to deploy docker images to jobs (which are in it's own ec2 instance)

## Test: 
---
This runs unittest for the api functions and makes sure the api's functionality is the way it's supposed to. 
```
docker-compose up scheduler-test
```
## Local Dev:
---
This is used as a local environment, also used for testing. It spins up a single container and runs the python app in debug mode for testing and developing. 
``` docker-compose up scheduler-dev ```

## Deployment:
---
### Terraform

The terraform scripts located in the *terraform* directory defines the iam policies and roles needed for the ec2 instance to run, and the ec2 instance it self. Run this command from your local machine to deploy the api to the associated aws cloud in the region of us-west-2. 

``` docker-compose up scheduler-deploy ```

* This spins up a new container containing dependecies like aws cli and terraform and runs the entrypoint. 
* The entrypoint will initiallize terraform with the backend state already saved in _sharbesh-terraform-state_ s3 bucket. Will then run a terraform plan and apply command. This terraform is set up to minimize down time with **create_before_destroy** set to **true**, terraform will first create a new instance before it destroys the old one. The output of the script will print out the instance id and public ip of the new instance. 

***note***: The terraform plan and apply uses the target flag for the ec2_instance because my aws account doesn't have permission to list policies which terraform needs to display the ouput, so it will fail. For this reason the target is set, this is not super importent at the moment because the terraform state in s3 will use the role that was created by me previously. 

### Docker-compose
This is used to deploy the production version of the application stack. This spins up 3 different containers:

* **a wusgi container**: serving the flask app for better stability and performance. The settings 	for the wusgi server including cached buffer size, multithreading and processes can be seen in _app.ini_ in the _scheduler_ folder. 
* **nginx container**: serves as an ingress for the app. This is the only container exposing any port (:80 in this case) on the host. The api and database containers can only be reached within the docker network created by docker-compose, so can only be reached by this nginx container. 
* **postgres container**: a database for persistance. This has a database schema called scheduler-jobs. 
