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

variable "cluster_ca_certificate" {
  description = "GKE cluster CA certificate"
  type        = string
  sensitive   = true
  default     = ""
}

variable "cluster_version" {
  description = "GKE cluster version"
  type        = string
  default     = ""
}

variable "deployments" {
  description = "List of deployments to create"
  type = list(object({
    name           = string
    image          = string
    replicas       = number
    port           = number
    cpu_request    = string
    cpu_limit      = string
    memory_request = string
    memory_limit   = string
    liveness_path  = string
    readiness_path = string
    env_vars       = optional(map(string))
    labels         = optional(map(string))
    annotations    = optional(map(string))
  }))
}

variable "services" {
  description = "List of services to create"
  type = list(object({
    name        = string
    port        = number
    type        = string
    labels      = optional(map(string))
    annotations = optional(map(string))
  }))
}

variable "enable_horizontal_pod_autoscaling" {
  description = "Enable HPA"
  type        = bool
  default     = true
}

variable "min_replicas" {
  description = "Minimum number of pods"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum number of pods"
  type        = number
  default     = 5
}

variable "target_cpu_utilization" {
  description = "Target CPU utilization percentage"
  type        = number
  default     = 70
}