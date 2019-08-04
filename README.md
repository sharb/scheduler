# Scheduler API

This api is used to deploy docker images to jobs (which are in it's own ec2 instance)

## Tests: 
---
#### pytest
* This runs unittest for the api functions and makes sure the api's functionality is the way it's supposed to.
#### flake8
* This is a linter to make sure all the standard coding format is met and the code is consistent throughout. The Config file to determine the formate is located in the **scheduler** folder in **flake8.ini**. 

These two tests can be performed with the docker-compose command below. These tests could also be used in a merge/pull request to secure/control the intregrety of the code. 
```
docker-compose up scheduler-test
```
## Local Dev:
---
This is used as a local environment, also used for testing. It spins up a single container and runs the python app in debug mode for testing and developing. 
``` docker-compose up scheduler-dev ```

## Secrets:
---
Secrets are stored in **.env** file in s3 bucket **s3://sharbesh-terraform-state/secrets/** . This is fetched during the creation and deployment of the instance inside _userdata_. 

secrets include the postgres database user and password: 
* POSTGRES_USER
* POSTGRES_PASSWORD

## Deployment:
---
### Terraform

The terraform scripts located in the *terraform* directory defines the iam policies and roles needed for the ec2 instance to run, and the ec2 instance it self. Run this command from your local machine to deploy the api to the associated aws cloud in the region of us-west-2. 

``` docker-compose up scheduler-deploy ```

* This spins up a new container containing dependecies like aws cli and terraform and runs the entrypoint. 
* The entrypoint will initiallize terraform with the backend state already saved in _sharbesh-terraform-state_ s3 bucket. Will then run a terraform plan and apply command. This terraform is set up to minimize down time with **create_before_destroy** set to **true**, terraform will first create a new instance before it destroys the old one. The output of the script will print out the instance id and public ip of the new instance. 

***note***: The terraform plan and apply uses the target flag for the ec2_instance because currently terraform is removing group name "kops" every terraform update and my user doesn't have **iam:DetachGroupPolicy** permission. This is not too big of a problem since although terraform errors out, it still created all the iam permission nessecerry for the scheduler api to work properly, and because of the **-target** flag terraform will not error. I also have the custom policy commented out from the **iam_rold.tf** file because for some reason I am still missing the **iam:CreatePolicy** permission. I was able to get around this by assigning preexisting aws owned policy. 


### Docker-compose
This is used to deploy the production version of the application stack. This spins up 3 different containers:

* **a wusgi container**: serving the flask app for better stability and performance. The settings 	for the wusgi server including cached buffer size, multithreading and processes can be seen in _app.ini_ in the _scheduler_ folder. 
* **nginx container**: serves as an ingress for the app. This is the only container exposing any port (:80 in this case) on the host. The api and database containers can only be reached within the docker network created by docker-compose, so can only be reached by this nginx container. 
* **postgres container**: a database for persistance. This has a database schema called scheduler-jobs. 
