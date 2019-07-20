import boto3, base64, sys

ec2 = boto3.resource('ec2', region_name='us-west-2')

def create_instance(job_name, json_data, mock):
    if(mock):
        print("Mock created aws Instance ######################## (mock) " + job_name, file=sys.stdout)
        # return json.loads('{"message": "Job creation Mocked")', 201
        return

    userdata = '''#!/bin/bash
                    sudo yum update -y
                    sudo yum install docker -y
                    sudo service docker start
                    sudo docker run -p 80:80 {}
        '''.format(json_data["image"])

    instances = ec2.create_instances(
        ImageId='ami-0f2176987ee50226e',
        InstanceType='t2.micro',
        UserData=userdata,
        MinCount=1,
        MaxCount=1,
        # KeyName='oregonKey',
        KeyName='se-devops-test',
        # SecurityGroupIds=['sg-74694311'],
        SecurityGroupIds=['sg-0c8ea569'],
        # DryRun=True,
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
    # return instances[0].id
    print("Created aws Instance ###############################################", file=sys.stdout)
    print(instances, file=sys.stdout)
    return 
    # return json.loads('{"message": "instance"' + str(delta) + '"}'), 201


# if __name__ == "__main__":
#     json_data = {
#         "image":"nginx", 
#         "time_scheduled":"now",
#         "status":"running"
#     }
#     job_name = "nginx"
#     create_instance(job_name, json_data, False)