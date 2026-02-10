variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "crypto-retirement"
}

variable "location" {
  description = "Region for the cluster (us-central1, europe-west1, etc)"
  type        = string
  default     = "us-central1"
}

variable "cluster_version" {
  description = "GKE cluster version"
  type        = string
  default     = "1.29.3-gke.30000001"
}

variable "network" {
  description = "VPC network to use (empty for default)"
  type        = string
  default     = ""
}

variable "subnetwork" {
  description = "VPC subnetwork to use (empty for default)"
  type        = string
  default     = ""
}

variable "enable_private_cluster" {
  description = "Enable private cluster (private nodes, no public endpoint)"
  type        = bool
  default     = false
}

variable "enable_private_endpoint" {
  description = "Enable private endpoint for control plane"
  type        = bool
  default     = false
}

variable "release_channel" {
  description = "Release channel (RAPID, REGULAR, STABLE)"
  type        = string
  default     = "REGULAR"
}

variable "enable_vertical_pod_autoscaling" {
  description = "Enable vertical pod autoscaling"
  type        = bool
  default     = true
}

variable "enable_workload_identity" {
  description = "Enable workload identity"
  type        = bool
  default     = true
}

variable "monitoring_service" {
  description = "Monitoring service (system, stackdriver, none)"
  type        = string
  default     = "system"
}

variable "logging_service" {
  description = "Logging service (system, stackdriver, none)"
  type        = string
  default     = "system"
}