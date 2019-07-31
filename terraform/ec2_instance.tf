

provider "aws" {
  region     = "us-west-2"
}

data "aws_ami" "amazon-linux-2" {
 most_recent = true
 owners      = ["137112412989"]

 filter {
   name   = "owner-alias"
   values = ["amazon"]
 }

 filter {
   name   = "name"
   values = ["amzn-ami-hvm-*-x86_64-gp2"]
 }
}

resource "aws_instance" "scheduler-api" {
    ami                         = "${data.aws_ami.amazon-linux-2.id}"
    associate_public_ip_address = true
    instance_type               = "t2.small"
    key_name                    = "se-devops-test"
    vpc_security_group_ids      = ["sg-0c8ea569"]
    iam_instance_profile   = "scheduler-profile"
    user_data = "${file("userdata.sh")}"
    tags = {
        Name = "Scheduler-Api"
    }
    lifecycle {
      create_before_destroy = true
    }
}

output "public_ip" {
  description = "Public IP of instance"
  value = coalesce(
    join("", aws_instance.scheduler-api.*.public_ip)
  )
}

output "instance_id" {
  description = "Disambiguated ID of the instance"
  value       = join("", aws_instance.scheduler-api.*.id)
}
