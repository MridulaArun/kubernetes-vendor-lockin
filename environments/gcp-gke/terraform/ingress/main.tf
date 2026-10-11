terraform {
  required_version = ">= 1.0.0"
}

resource "null_resource" "mock_gcp_ingress" {
  count = 0
}
