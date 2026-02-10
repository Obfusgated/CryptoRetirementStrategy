resource "google_storage_bucket" "web" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = var.force_destroy
  storage_class = var.storage_class

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  versioning {
    enabled = var.enable_versioning
  }

  lifecycle_rule {
    id     = "cleanup"
    action = "Delete"

    condition {
      age_days = 30
    }

    enabled = var.lifecycle_rule_enabled
  }

  uniform_bucket_level_access = var.public_access_prevention
}

# IAM policy for GKE workload identity to access bucket
resource "google_storage_bucket_iam_binding" "public" {
  count = var.public_access_prevention ? 1 : 0

  bucket = google_storage_bucket.web.name
  role   = "roles/storage.objectViewer"

  members = [
    "allUsers"
  ]
}

resource "google_storage_bucket_iam_binding" "gke" {
  bucket = google_storage_bucket.web.name
  role   = "roles/storage.objectViewer"

  dynamic "members" {
    for_each = var.gke_service_accounts

    content = "serviceAccount:${each.value}"
  }
}