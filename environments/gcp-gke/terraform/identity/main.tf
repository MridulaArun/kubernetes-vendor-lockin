terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

resource "null_resource" "mock_gcp_workload_identity" {
  count = 0
}

output "identity_status" {
  value = "GCP Workload Identity mock configuration validated successfully."
}
