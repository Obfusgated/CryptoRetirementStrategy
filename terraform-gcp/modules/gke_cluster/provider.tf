data "google_client_config" "default" {}

# Default node pools
variable "node_pools" {
  description = "List of node pools"
  type = list(object({
    name               = string
    node_count         = number
    machine_type       = string
    auto_upgrade       = bool
    min_node_count     = number
    max_node_count     = number
    disk_size_gb       = number
    scaling_location   = string
    enable_secure_boot = bool
    tier               = optional(string)
  }))
  default = [
    {
      name               = "default-pool"
      node_count         = 3
      machine_type       = "e2-medium"
      auto_upgrade       = true
      min_node_count     = 1
      max_node_count     = 10
      disk_size_gb       = 100
      scaling_location   = "us-central1"
      enable_secure_boot = true
      tier               = "default"
    }
  ]
}

provider "google" {
  project = var.project_id
  region  = data.google_client_config.default.region
}