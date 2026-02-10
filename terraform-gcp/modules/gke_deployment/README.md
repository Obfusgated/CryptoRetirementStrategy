# GKE Deployment Module

Creates deployments, services, and optional configmaps for the Crypto Retirement app.

## Usage

```hcl
module "gke_deployment" {
  source = "../gke_deployment"

  namespace = "crypto-retirement"

  deployments = [
    {
      name           = "crypto-retirement-web"
      image          = "us-central1-docker.pkg.dev/your-registry/crypto-retirement:latest"
      replicas       = 2
      port           = 80
      cpu_request    = "250m"
      cpu_limit      = "500m"
      memory_request = "256Mi"
      memory_limit  = "512Mi"
      liveness_path  = "/"
      readiness_path  = "/"
    }
  ]

  services = [
    {
      name           = "crypto-retirement-web"
      port           = 80
      type           = "ClusterIP"
    }
  ]

  enable_horizontal_pod_autoscaling = true
  min_replicas                          = 1
  max_replicas                          = 5
  target_cpu_utilization               = 70
}
```

## Requirements

| Name | Version |
|------|---------|
| kubernetes | >= 1.24 |

## Outputs

| Name | Description |
|------|-------------|
| namespace | Kubernetes namespace |
| deployment_names | List of deployment names |
| service_names | List of service names |
| hpa_enabled | Whether HPA is enabled |