terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "mock_aks_cluster" {
  count = 0
}

output "mock_aks_status" {
  value = "AKS static configuration parsed successfully."
}

