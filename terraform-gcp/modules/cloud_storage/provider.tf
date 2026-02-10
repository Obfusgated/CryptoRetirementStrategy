variable "gke_service_accounts" {
  description = "List of GKE workload identity service accounts"
  type        = list(string)
  default     = []
}