variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "bucket_name" {
  description = "GCS bucket name"
  type        = string
  default     = "crypto-retirement-web"
}

variable "location" {
  description = "Bucket location (US, EU, ASIA, etc)"
  type        = string
  default     = "US"
}

variable "storage_class" {
  description = "Storage class"
  type        = string
  default     = "STANDARD"

  validation {
    condition     = contains(["STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"], var.storage_class)
    error_message = "storage_class must be STANDARD, NEARLINE, COLDLINE, or ARCHIVE"
  }
}

variable "force_destroy" {
  description = "Allow force delete of bucket"
  type        = bool
  default     = true
}

variable "enable_versioning" {
  description = "Enable object versioning"
  type        = bool
  default     = false
}

variable "lifecycle_rule_enabled" {
  description = "Enable lifecycle rule to delete old objects"
  type        = bool
  default     = true
}

variable "public_access_prevention" {
  description = "Prevent public access"
  type        = bool
  default     = true
}