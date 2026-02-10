# Terraform configuration for GCP
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
      project = var.project_id
      region  = var.region
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"

      config_path            = "${pathexpand("~")}/.kube/config"
      host                   = module.gke_cluster.cluster_endpoint
      cluster_ca_certificate = base64decode(module.gke_cluster.cluster_ca_certificate)
    }
  }

  required_version = ">= 1.0"
}

# Local backend state
terraform {
  backend "local" {
    path = "terraform-gcp/terraform.tfstate"
  }
}