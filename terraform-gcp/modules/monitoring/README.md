# Monitoring Module

Creates Cloud Logging and Cloud Monitoring setup for the Crypto Retirement app.

## Features

- Cloud Logging for application logs
- Cloud Monitoring for metrics
- Log-based metrics
- Dashboard configuration

## Usage

```hcl
module "monitoring" {
  source = "../monitoring"

  project_id  = "your-project-id"
  cluster_name = "crypto-retirement"
  namespace   = "crypto-retirement"

  enable_logging  = true
  enable_monitoring = true

  logging = {
    log_sink_name    = "crypto-retirement-logs"
    retention_period = "30d"
  }

  monitoring = {
    monitored_project_name = "crypto-retirement"
    dashboard_name         = "crypto-retirement-dashboard"

    metrics = [
      "container.cpu/usage",
      "container.memory/working_set_bytes"
      "container.memory/cache_bytes"
      "kubernetes.pod.running_count"
    ]
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| google | ~> 5.0 |

## Outputs

| Name | Description |
|------|-------------|
| log_sink_name | Cloud Logging sink name |
| logging_enabled | Whether logging is enabled |
| monitoring_enabled | Whether monitoring is enabled |
| project_id | Monitored project ID |