# Cloudflare Tunnel Ingress (Recommended for privacy-first)

# Create Cloudflare resources
module "cloudflare_resources" {
  count  = var.ingress_type == "cloudflare-tunnel" ? 1 : 0
  source = "./cloudflare"

  tunnel_id    = var.cloudflare_tunnel_id
  service_name = var.service_name
  service_port = var.service_port
  namespace    = var.namespace

  account_token = var.cloudflare_account_token
}

# GKE Ingress Controller
resource "kubernetes_ingress_v1" "gke" {
  count = var.ingress_type == "gke-ingress" ? 1 : 0

  metadata {
    name      = "crypto-retirement-ingress"
    namespace = kubernetes_namespace.default.metadata[0].name
    labels = {
      app = "crypto-retirement"
    }
  }

  spec {
    default_backend {
      service {
        name = var.service_name
        port {
          number = var.service_port
        }
      }
    }

    rule {
      host = var.domain_name != "" ? var.domain_name : "crypto-retirement-ingress.nip.io"
      http {
        path      = "/"
        path_type = "Prefix"
        backend {
          service {
            name = var.service_name
            port {
              number = var.service_port
            }
          }
        }
      }
    }
  }

  tls {
    secret_name = var.ssl_cert_secret
  }
}

# Static IP for GKE Ingress (optional)
resource "google_compute_global_address" "static" {
  count = var.ingress_type == "gke-ingress" && var.static_ip == "" ? 1 : 0

  name = var.cluster_name

  address_type = "IPV4"
  description  = "Static IP for ${var.cluster_name} crypto-retirement app"
}