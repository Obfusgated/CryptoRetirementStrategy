variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "crypto-retirement"
}

variable "cluster_name" {
  description = "GKE cluster name"
  type        = string
  default     = "crypto-retirement"
}

variable "cluster_endpoint" {
  description = "GKE cluster endpoint"
  type        = string
}

variable "cluster_version" {
  description = "GKE cluster version"
  type        = string
  default     = ""
}

variable "ingress_type" {
  description = "Type of ingress: cloudflare-tunnel or gke-ingress"
  type        = string
  default     = "cloudflare-tunnel"

  validation {
    condition     = contains(["cloudflare-tunnel", "gke-ingress"], var.ingress_type)
    error_message = "ingress_type must be cloudflare-tunnel or gke-ingress"
  }
}

variable "service_name" {
  description = "Name of the backend Kubernetes service"
  type        = string
}

variable "service_port" {
  description = "Port of the backend service"
  type        = number
  default     = 80
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "cloudflare_tunnel_id" {
  description = "Cloudflare tunnel ID (for cloudflare-tunnel)"
  type        = string
  default     = ""
}

variable "cloudflare_account_token" {
  description = "Cloudflare account token"
  type        = string
  sensitive   = true
}

variable "static_ip" {
  description = "Static IP address for gke-ingress (empty for auto-provision)"
  type        = string
  default     = ""
  sensitive   = true
}

variable "enable_ssl" {
  description = "Enable SSL/TLS"
  type        = bool
  default     = true
}

variable "ssl_cert_secret" {
  description = "Kubernetes secret name for SSL certificate"
  type        = string
  default     = "crypto-retirement-ssl"
}