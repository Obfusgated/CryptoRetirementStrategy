output "bucket_name" {
  description = "GCS bucket name"
  value       = google_storage_bucket.web.name
}

output "bucket_url" {
  description = "HTTPS URL to access bucket"
  value       = "https://storage.googleapis.com/${google_storage_bucket.web.name}"
}

output "location" {
  description = "Bucket location"
  value       = google_storage_bucket.web.location
}

output "lifecycle_rule_enabled" {
  description = "Whether lifecycle rule is enabled"
  value       = var.lifecycle_rule_enabled
}