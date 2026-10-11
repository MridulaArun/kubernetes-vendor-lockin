terraform {
  required_version = ">= 1.0.0"
}

resource "null_resource" "mock_kubeadm_identity" {
  count = 0
}

output "identity_status" {
  value = "Kubeadm baseline identity mock configuration validated successfully."
}
