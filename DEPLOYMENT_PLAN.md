# Development & Deployment Plan

## Environments

### 1. Local Kubernetes (Development/Testing)
- Kind or Minikube for local Kubernetes
- Docker container for the crypto app
- Manifest-based deployment
- Fast iteration, no cloud costs

### 2. GKE (Production POC)
- Google Kubernetes Engine on GCP
- Managed control plane for production
- Terraform infrastructure-as-code
- Cloudflare Ingress Controller (alternative to GLBC)

## Data Privacy Strategy: Stateless Cloud

**Architecture:**
- Cloud servers: Only serve static HTML/JS/CSS files
- All processing: Happens in user's browser
- Tax lots: Stored in localStorage/IndexedDB on user's device
- MCP AI server: Direct browser connection (10.0.0.209)

**Advantages:**
- User data never reaches cloud servers
- Zero data retention requirements
- Simpler compliance
- Lower cloud costs

## Module Structure

```
crypto-retirement/
├── terraform-gcp/
│   ├── modules/
│   │   ├── gke_cluster/
│   │   ├── gke_deployment/
│   │   ├── ingress/
│   │   │   ├── cloudflare/
│   │   │   └── gke/
│   │   ├── cloud_storage/
│   │   └── monitoring/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── local-k8s/
│   ├── Dockerfile
│   ├── k8s-manifests/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── docker-compose.yml
│   ├── scripts/
│   │   ├── deploy-local.sh
│   │   └── destroy-local.sh
│   └── README.md
└── kubernetes/
    ├── deployment/
    ├── service/
    └── ingress
```

## Implementation Order

### Phase 1: Local Kubernetes (Fast feedback) ✅
1. Dockerfile for crypto app container ✅
2. k8s manifests for local deployment ✅
3. Scripts to spin up Kind cluster
4. Test locally with live reload

### Phase 2: GKE Terraform Modules (In Progress)
1. Dockerfile for crypto app container
2. k8s manifests for local deployment
3. Scripts to spin up Kind cluster
4. Test locally with live reload

### Phase 2: GKE Terraform Modules
1. gke_cluster module (cluster creation)
2. gke_deployment module (namespace, deployments, services)
3. ingress module (Cloudflare or GKE Ingress)
4. cloud_storage module (GCS for static assets)
5. monitoring module (Cloud Logging/Monitoring)

### Phase 3: POC Deployment
1. Containerize crypto app
2. Push to GCR
3. Deploy to GKE
4. Configure Ingress
5. TLS certificates

Let me know to start with Phase 1 (local environment) or Phase 2 (GKE modules) first?