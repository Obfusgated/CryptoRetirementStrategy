output "namespace_created" {
  description = "Kubernetes namespace created"
  value       = kubernetes_namespace.default.metadata[0].name
}

output "deployment_names" {
  description = "List of deployment names"
  value       = [kubernetes_deployment.main[*].metadata[*].name]
}

output "service_names" {
  description = "List of service names"
  value       = [kubernetes_service.main[*].metadata[*].name]
}

output "hpa_enabled" {
  description = "Whether HPA is enabled"
  value       = var.enable_horizontal_pod_autoscaling
}

output "kubeconfig_command" {
  description = "Command to generate kubeconfig"
  value       = "gcloud container clusters get-credentials ${var.cluster_name} --region ${data.google_client_config.default.region} --zone ${data.google_client_config.default.zone}"
}

output "kubectl_context_command" {
  description = "Command to configure kubectl context"
  value       = "kubectl config use-context gke_${var.region}_${var.cluster_name}"
}