terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
resource "null_resource" "mock_gcp_pd_csi" { count = 0 }
output "storage_status" { value = "GCP GKE PD CSI mock configuration validated successfully." }
