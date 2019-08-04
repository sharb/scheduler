import boto3, sys

ec2 = boto3.resource('ec2', region_name='us-west-2')


# This function will return after either mock instance or real instance has been created
def create_instance(job_name, json_data, mock):
    if(mock):
        print("Mock created aws Instance ######################## (mock) " + job_name, file=sys.stdout)
        return

    # userdata mainly to run the given image
    userdata = '''#!/bin/bash
                    sudo yum update -y
                    sudo yum install docker -y
                    sudo service docker start
                    sudo docker run -p 80:80 {}
        '''.format(json_data["image"])

    # creats instance with the name of the job
    # this will tag:Createdby with the value of "Scheduler-Api"
    ec2.create_instances(
        ImageId='ami-0f2176987ee50226e',
        InstanceType='t2.micro',
        UserData=userdata,
        MinCount=1,
        MaxCount=1,
        KeyName='se-devops-test',
        SecurityGroupIds=['sg-0c8ea569'],
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': job_name
                    },
                    {
                        'Key': 'Createdby',
                        'Value': "Scheduler-Api"
                    }
                ]
            }
        ]
    )
    return
