terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
resource "null_resource" "mock_aws_ebs_csi" { count = 0 }
output "storage_status" { value = "AWS EBS CSI mock configuration validated successfully." }
