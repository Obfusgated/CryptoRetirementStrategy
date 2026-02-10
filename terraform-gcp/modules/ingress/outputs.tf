output "ingress_created" {
  description = "Ingress resource created"
  value       = try(kubernetes_ingress.cloudflare_tunnel[*].metadata[*].name, kubernetes_ingress.gke[*].metadata[*].name, [])
}

output "ingress_url" {
  description = "Full URL to access the application"
  value       = format(
    "https://%s%s",
    var.domain_name != "" ? "${var.domain_name}/" : "",
    ingressing_ip != "" ? replace(
      split(ingressing_ip, "/")[0],
      /[0-9]+$/,
      "crypto-retirement"
    ) : "${var.service_name}.${var.namespace}.svc.cluster.local"
  )
}

output "ingressing_ip" {
  description = "External IP address"
  value       = try(
    replace(
      google_compute_global_address.static[*].address,
      /[0-9]+/,
      "crypto-retirement"
    ),
    "",
  )
}

output "tls_enabled" {
  description = "Whether TLS is enabled"
  value       = var.enable_ssl
}

data "google_client_config" "default" {}