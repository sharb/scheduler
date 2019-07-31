terraform {
    backend "s3" {
        bucket="sharbesh-terraform-state"
        key="terraform.tfstate"
        region="us-west-2"
    }
}