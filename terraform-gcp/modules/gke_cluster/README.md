# GKE Cluster Module

Provisions a Google Kubernetes Engine cluster for the Crypto Retirement app.

## Usage

```hcl
module "gke_cluster" {
  source = "../gke_cluster"

  cluster_name    = "crypto-retirement"
  location        = "us-central1"
  cluster_version = "1.29.3-gke.30000001"

  node_pools = [
    {
      name         = "default-pool"
      node_count   = 3
      machine_type = "e2-medium"
      auto_upgrade = true
      disk_size_gb = 100
    }
  ]

  enable_vertical_pod_autoscaling = true
  enable_private_cluster = false
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| google | ~> 5.0 |

## Outputs

| Name | Description |
|------|-------------|
| cluster_id | GKE cluster ID |
| endpoint | Cluster API endpoint |
| ca_certificate | Cluster CA certificate |
| status | Cluster status |