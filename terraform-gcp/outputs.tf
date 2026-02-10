output "cluster_name" {
  description = "GKE cluster name"
  value       = module.gke_cluster.cluster_name
}

output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = module.gke_cluster.cluster_endpoint
}

output "cluster_ca_certificate" {
  description = "GKE cluster CA certificate"
  value       = module.gke_cluster.cluster_ca_certificate
}

output "cluster_version" {
  description = "GKE cluster version"
  value       = module.gke_cluster.cluster_version
}

output "ingress_url" {
  description = "Application URL"
  value       = module.ingress.ingress_url
}

output "ingress_ip" {
  description = "External IP"
  value       = module.ingress.ingressing_ip
}

output "bucket_url" {
  description = "Cloud Storage URL"
  value       = module.cloud_storage.bucket_url
}

output "logging_enabled" {
  description = "Cloud Logging enabled"
  value       = module.monitoring.logging_enabled
}

output "log_sink_name" {
  description = "Cloud Logging sink name"
  value       = module.monitoring.log_sink_name
}

output "gke_context_command" {
  description = "Command to configure kubectl context"
  value       = "${module.gke_deployment.kubectl_context_command}\nkubectl config use-context ${module.gke_deployment.kubectl_context}"
}