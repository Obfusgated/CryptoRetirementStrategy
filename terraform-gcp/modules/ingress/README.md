# Ingress Module

Creates Ingress resources for routing external traffic to the Crypto Retirement app.

## Options

### Cloudflare Ingress (Recommended)
- Cloudflare Tunnel with Argo Tunnel
- No Kubernetes Ingress Controller needed
- Global CDN
- SSL/TLS managed automatically

### GKE Ingress Controller
- GKE Ingress Controller (L7 GLBC)
- Managed ingress on GCP
- Single IP for load balancing
- SSL cert integration

## Usage

```hcl
module "ingress" {
  source = "../ingress"

  ingress_type    = "cloudflare-tunnel"
  cluster_name    = "crypto-retirement"
  service_name    = "crypto-retirement-web"
  service_port    = 80
  cluster_endpoint = var.cluster_endpoint

  domain_name     = "crypto-retirement.example.com"

  cloudflare_config = {
    tunnel_id      = var.cloudflare_tunnel_id
    account_token = var.cloudflare_account_token
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| kubernetes | >= 1.19 |
| terraform | >= 1.0 |
| google | ~> 5.0 |

## Outputs

| Name | Description |
|------|-------------|
| ingress_name | Ingress resource name |
| ingressing_ip | External IP address |
| ingress_url | Full URL to access the application |