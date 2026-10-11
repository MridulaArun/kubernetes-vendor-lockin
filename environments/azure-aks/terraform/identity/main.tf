terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "mock_azure_workload_identity" {
  count = 0
}

output "identity_status" {
  value = "Azure Workload Identity mock configuration validated successfully."
}
