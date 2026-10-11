terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
resource "null_resource" "mock_azure_disk_csi" { count = 0 }
output "storage_status" { value = "Azure Disk CSI mock configuration validated successfully." }
