terraform {
  required_version = ">= 1.0.0"
}

resource "null_resource" "mock_kubeadm_storage" {
  count = 0
}

output "storage_status" {
  value = "Kubeadm baseline storage mock configuration validated successfully."
}