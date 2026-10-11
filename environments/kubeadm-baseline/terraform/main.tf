terraform {
  required_version = ">= 1.0.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "kubeadm_manifest_baseline" {
  filename = "${path.module}/kubeadm-config-baseline.yaml"
  content  = <<-EOT
    apiVersion: kubeadm.k8s.io/v1beta3
    kind: ClusterConfiguration
    controlPlaneEndpoint: "192.168.56.10:6443"
    networking:
      podSubnet: "10.244.0.0/16"
      serviceSubnet: "10.96.0.0/12"
  EOT
}

output "mock_kubeadm_status" {
  value = "Kubeadm self-managed baseline configuration generated successfully."
}