resource "google_service_project" "service" {
  project                    = var.project_id
  project_id                 = var.project_id
  description                = "GKE cluster"
  disable_dependent_services = false
  disable_on_destroy         = false
}

resource "google_container_cluster" "main" {
  name        = var.cluster_name
  location    = var.location
  project     = var.project_id
  description = "Crypto Retirement Web App"

  initial_node_count       = 3
  remove_default_node_pool = true

  network    = var.network != "" ? var.network : null
  subnetwork = var.subnetwork != "" ? var.subnetwork : null

  master_auth {
    username = ""
    client_certificate_config {
      issue_client_certificate = false
    }
  }

  addons_config {
    horizontal_pod_autoscaling {
      disabled = false
    }
    gcp_filestore_csi_driver_config {
      enabled = true
    }
  }

  node_config {
    machine_type = "e2-medium"
    disk_type    = "pd-balanced"
    disk_size_gb = 100
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    shielded_instance_config {
      enable_secure_boot = true
    }
  }

  workload_identity_config {
    workload_pool = var.enable_workload_identity ? "PROJECT_ID.svc.id.googlesusercontent.com" : ""
  }

  vertical_pod_autoscaling = var.enable_vertical_pod_autoscaling
  enable_private_endpoint  = var.enable_private_endpoint
  private_cluster          = var.enable_private_cluster

  release_channel {
    channel = var.release_channel
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = var.monitoring_service == "system"
    }
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
    managed_logging {
      enabled = var.logging_service == "system"
    }
  }

  timeouts {
    create = "30m"
    update = "40m"
    delete = "60m"
  }
}

resource "google_container_node_pool" "node_pools" {
  for_each = var.node_pools

  name     = "${google_container_cluster.main.name}-${each.value.name}"
  location = google_container_cluster.main.location
  cluster  = google_container_cluster.main.name
  project  = google_container_cluster.main.project

  version = google_container_cluster.main.version

  node_count         = each.value.node_count
  initial_node_count = each.value.auto_upgrade ? 1 : each.value.node_count

  node_config {
    machine_type = each.value.machine_type
    disk_type    = "pd-balanced"
    disk_size_gb = each.value.disk_size_gb
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    shielded_instance_config {
      enable_secure_boot = each.value.enable_secure_boot
    }
    resource_labels = {
      tier = each.value.tier
    }
  }

  management {
    auto_repair  = true
    auto_upgrade = each.value.auto_upgrade
  }

  autoscaling {
    min_node_count = each.value.min_node_count
    max_node_count = each.value.max_node_count
    location       = each.value.scaling_location
  }

  upgrade_settings {
    max_surge       = 1
    max_unavailable = 0
  }

  lifecycle {
    ignore_changes = all[
      google_container_node_pool.node_pools[each.key].node_config
    ]
  }
}