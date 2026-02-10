# Get GCP client config
data "google_client_config" "default" {}

resource "google_project_service" "services" {
  project = var.project_id
  
  services = [
    "cloudkms.googleapis.com",
    "container.googleapis.com",
    "containerfilesystem.googleapis.com",
  ]
  
  disable_on_destroy = false
  disable_dependent_services = false
}

# GKE Cluster Module
module "gke_cluster" {
  source = "./modules/gke_cluster"

  project_id     = var.project_id
  cluster_name  = var.cluster_name
  cluster_version = "1.29.3-gke.30000001"
  region          = var.region
  location        = var.region

  node_pools = [
    {
      name           = "default-pool"
      node_count      = 3
      machine_type    = "e2-medium"
      auto_upgrade    = true
      min_node_count  = 1
      max_node_count  = 10
      disk_size_gb    = 100
      scaling_location = var.region
      enable_secure_boot = true
      tier             = "default"
    }
  ]

  enable_vertical_pod_autoscaling = true
  enable_workload_identity          = true
  enable_private_cluster           = false
}

# Workload Identity (for serverless later)
module "workload_identity" {
  count = var.environment == "dev" ? 1 : 0
  source = "./workload_identity"

  project_id = var.project_id
  namespace  = var.namespace
}

# GKE Deployment Module
module "gke_deployment" {
  source = "./modules/gke_deployment"

  project_id        = var.project_id
  cluster_name      = module.gke_cluster.cluster_name
  cluster_endpoint   = module.gke_cluster.cluster_endpoint
  cluster_ca_certificate = module.gke_cluster.cluster_ca_certificate
  namespace          = var.namespace

  deployments = [
    {
      name            = "crypto-retirement-web"
      image           = var.image
      image_pull_policy = "IfNotPresent"
      replicas        = 2
      port            = 80
      cpu_request     = "250m"
      cpu_limit       = "500m"
      memory_request  = "256Mi"
      memory_limit    = "512Mi"
      liveness_path   = "/"
      readiness_path   = "/"
    }
  ]

  services = [
    {
      name    = "crypto-retirement-web"
      port    = 80
      type    = "ClusterIP"
    }
  ]

  enable_horizontal_pod_autoscaling = true
  min_replicas                          = 1
  max_replicas                          = 5
  target_cpu_utilization               = 70
}

# Cloud Storage Module
module "cloud_storage" {
  project_id = var.project_id

  bucket_name     = "crypto-retirement-web-${lower(var.environment)}"
  location       = "US"
  storage_class  = "STANDARD"
  force_destroy  = true

  lifecycle_rule_enabled = true
}

# Ingress Module
module "ingress" {
  source = "./modules/ingress"

  project_id           = var.project_id
  cluster_name          = module.gke_cluster.cluster_name
  namespace            = var.namespace
  cluster_endpoint      = module.gke_cluster.cluster_endpoint
  cluster_ca_certificate = module.gke_cluster.cluster_ca_certificate

  ingress_type           = var.ingress_type

  service_name           = "crypto-retirement-web"
  service_port           = 80

  domain_name            = var.domain_name

  cloudflare_tunnel_id    = var.cloudflare_tunnel_id
  cloudflare_account_token = var.cloudflare_account_token

  enable_ssl              = true
  ssl_cert_secret         = "crypto-retirement-ssl"

  static_ip              = ""
}

# Monitoring Module
module "monitoring" {
  project_id  = var.project_id
  namespace   = var.namespace
  cluster_name = module.gke_cluster.cluster_name

  enable_logging  = true
  enable_monitoring = true

  logging = {
    log_sink_name    = "crypto-retirement-logs"
    retention_period = "30d"
  }

  monitoring = {
    monitored_project_name = "crypto-retirement-${var.environment}"
    dashboard_name         = "crypto-retirement-dashboard"
  }