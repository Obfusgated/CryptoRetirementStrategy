# Create namespace
resource "kubernetes_namespace" "default" {
  metadata {
    name = var.namespace
    labels = {
      app = "crypto-retirement"
    }
  }
}

# Create deployments
resource "kubernetes_deployment" "main" {
  for_each = var.deployments

  metadata {
    name      = each.value.name
    namespace = kubernetes_namespace.default.metadata[0].name
    labels = merge({
      app = "crypto-retirement"
      component = "web"
    }, each.value.labels)
  }

  spec {
    replicas = each.value.replicas

    selector {
      match_labels = merge({
        app = "crypto-retirement"
        component = "web"
      }, each.value.labels)
    }

    template {
      metadata {
        labels = merge({
          app = "crypto-retirement"
          component = "web"
        }, each.value.labels)
        annotations = merge({
          "autoscaling.kubernetes.io/scale-down-disabled" = "false"
        }, each.value.annotations)
      }

      spec {
        container {
          name  = each.value.name
          image = each.value.image
          ports {
            container_port = each.value.port
          }
          env = each.value.env_vars

          resources {
            limits = {
              cpu    = each.value.cpu_limit
              memory = each.value.memory_limit
            }
            requests = {
              cpu    = each.value.cpu_request
              memory = each.value.memory_request
            }
          }

          liveness_probe {
            http_get {
              path = each.value.liveness_path
              port = each.value.port
            }
            initial_delay_seconds = 10
            period_seconds        = 30
          }

          readiness_probe {
            http_get {
              path = each.value.readiness_path
              port = each.value.port
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          security_context {
            allow_privilege_escalation = false
            run_as_user               = 1000
            run_as_group              = 1000
          }
        }
      }
    }
  }
}

# Enable HPA if requested
resource "kubernetes_horizontal_pod_autoscaler" "main" {
  count = var.enable_horizontal_pod_autoscaling ? 1 : 0

  for_each = toset(kubernetes_deployment.main[*].metadata)

  metadata {
    name = "${each.value.name}-hpa"
    namespace = kubernetes_namespace.default.metadata[0].name
  }

  spec {
    max_replicas                  = var.max_replicas
    min_replicas                  = var.min_replicas
    scale_target_ref {
      api_version = "apps/v1"
      kind       = "Deployment"
      name       = each.value.name
    }
    target_cpu_utilization_percentage = var.target_cpu_utilization

    behavior {
      scale_down {
        stabilization_window_seconds = 300
        policies = [
          {
            type           = "Pods"
            value          = 2
            period_seconds = 60
          },
          {
            type           = "Percent"
            value          = 50
            period_seconds = 60
          }
        ]
      }
    }

    metrics {
      pods {
        metric {
          type = "Resource"
          resource {
            name = "cpu"
      }

        metrics {
          type = "Resource"
          resource {
            name = "memory"
}}