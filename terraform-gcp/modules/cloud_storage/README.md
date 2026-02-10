# Cloud Storage Module

Creates GCS bucket for serving static web assets for the Crypto Retirement app.

## Usage

```hcl
module "cloud_storage" {
  source = "../cloud_storage"

  bucket_name     = "crypto-retirement-web"
  location       = "US"
  storage_class  = "STANDARD"
  force_destroy  = true

  lifecycle_rule {
    id      = "cleanup"
    action  = "Delete"
    enabled = true
  }
}
```

## Private vs Public Bucket

| Type | Use Case | Access Control |
|------|---------|---------------|
| Public | Static HTML/JS files serving from GKE | public-read |
| Private | (if server-side processing needed) | GKE workload identity |

**Recommendation: Public bucket for stateless architecture**

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| google | ~> 5.0 |

## Outputs

| Name | Description |
|------|-------------|
| bucket_name | GCS bucket name |
| bucket_url | HTTPS URL to access bucket contents |
| location | Bucket location |