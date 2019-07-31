#! /bin/bash
sudo yum update -y
sudo yum install git -y
sudo git clone https://github.com/sharb/scheduler.git /home/ec2-user/scheduler
sudo yum install docker -y
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /home/ec2-user/scheduler/docker-compose
sudo chmod +x /home/ec2-user/scheduler/docker-compose
cd /home/ec2-user/scheduler/
sudo /home/ec2-user/scheduler/docker-compose up -d scheduler-prod