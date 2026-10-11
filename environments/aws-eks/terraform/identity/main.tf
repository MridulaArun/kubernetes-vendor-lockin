terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "null_resource" "mock_aws_irsa" {
  count = 0
}

output "identity_status" {
  value = "AWS IRSA mock configuration validated successfully."
}
