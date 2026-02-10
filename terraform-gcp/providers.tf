provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "kubernetes" {
  config_path            = "${pathexpand("~")}/.kube/config"
  host                   = null # Set dynamically during apply
  cluster_ca_certificate = null # Set dynamically

  exec {
    dynamic "cluster_endpoint" {
      query = module.gke_cluster.cluster_endpoint
    }
  }

  exec {
    dynamic "host" {
      query = module.gke_cluster.cluster_endpoint
    }
  }

  exec {
    dynamic "cluster_ca_certificate" {
      query = module.gke_cluster.cluster_ca_certificate
    }
  }
}