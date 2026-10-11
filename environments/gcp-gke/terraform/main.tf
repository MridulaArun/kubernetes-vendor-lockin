terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = "mock-gcp-project"
  region      = "asia-south1"
  credentials = jsonencode({
    type = "service_account"
  })
}

resource "google_container_cluster" "mock_gke" {
  count    = 0
  name     = "nimbus-dummy-gke-cluster"
  location = "asia-south1-a"
}

output "mock_gke_status" {
  value = "GKE static configuration parsed successfully."
}