terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "ap-south-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

resource "aws_eks_cluster" "mock_eks" {
  count    = 0
  name     = "nimbus-dummy-eks-cluster"
  role_arn = "arn:aws:iam::000000000000:role/dummy-role"

  vpc_config {
    subnet_ids = ["subnet-00000000", "subnet-11111111"]
  }
}

output "mock_cluster_status" {
  value = "EKS static configuration parsed successfully for vendor lock-in analysis."
}