resource "aws_iam_role" "scheduler-role" {
  name               = "scheduler-role"
  assume_role_policy = "${file("assume-role-policy.json")}"
}

# resource "aws_iam_policy" "ec2_iam_policy" {
#   name        = "ec2_iam_policy"
#   description = "ec2 admin access policy"
#   policy      = "${file("ec2_policy.json")}"
# }

resource "aws_iam_policy_attachment" "attach-to-scheduler" {
  name       = "attach-to-scheduler"
  roles      = ["${aws_iam_role.scheduler-role.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
  # policy_arn = "${aws_iam_policy.ec2_iam_policy.arn}"
}

resource "aws_iam_policy_attachment" "attach-to-scheduler-s3" {
  name       = "attach-to-scheduler"
  roles      = ["${aws_iam_role.scheduler-role.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "scheduler-profile" {
  name  = "scheduler-profile"
  roles = ["${aws_iam_role.scheduler-role.name}"]
}