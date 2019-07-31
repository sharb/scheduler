resource "aws_iam_role" "scheduler-role" {
  name               = "scheduler-role"
  assume_role_policy = "${file("assume-role-policy.json")}"
}

resource "aws_iam_policy" "ec2-policy" {
  name        = "ec2-policy"
  description = "ec2 admin access policy"
  policy      = "${file("ec2_iam_policy.json")}"
}

resource "aws_iam_policy_attachment" "attach-to-scheduler" {
  name       = "attach-to-scheduler"
  roles      = ["${aws_iam_role.scheduler-role.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_instance_profile" "scheduler-profile" {
  name  = "scheduler-profile"
  roles = ["${aws_iam_role.scheduler-role.name}"]
}