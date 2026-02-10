variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region (required)"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "cluster_name" {
  description = "GKE cluster name"
  type        = string
  default     = "crypto-retirement"
}

variable "cloudflare_tunnel_id" {
  description = "Cloudflare tunnel ID (for cloudflare-tunnel ingress)"
  type        = string
  default     = ""
}

variable "cloudflare_account_token" {
  description = "Cloudflare account token (starts with CF-)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "ingress_type" {
  description = "Ingress type"
  type        = string
  default     = "cloudflare-tunnel"

  validation {
    condition     = contains(["cloudflare-tunnel", "gke-ingress"], var.ingress_type)
    error_message = "ingress_type must be cloudflare-tunnel or gke-ingress"
  }
}

variable "image" {
  description = "Docker image for the application"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}