#!/bin/bash

# Deploy Crypto Retirement App to Local Kubernetes

set -e

echo "🚀 Deploying Crypto Retirement to Local Kubernetes..."

# Create Kind cluster if it doesn't exist
if ! kind get clusters 2>/dev/null | grep -q "crypto-retirement"; then
    echo "Creating Kind cluster crypto-retirement..."
    kind create cluster --name crypto-retirement --config kind-config.yaml
fi

# Build Docker image
echo "Building Docker image..."
docker build -t crypto-retirement:latest .

# Load image into Kind
echo "Loading image into Kind..."
kind load docker-image crypto-retirement:latest --name crypto-retirement

# Apply manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f local-k8s/k8s-manifests/deployment.yaml
kubectl apply -f local-k8s/k8s-manifests/service.yaml
kubectl apply -f local-k8s/k8s-manifests/ingress.yaml

# Wait for deployment
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/crypto-retirement-web -n crypto-retirement --timeout=300s

# Get ingress URL
INGRESS_IP=$(kubectl get ingress crypto-retirement-ingress -n crypto-retirement -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Access the app at: http://crypto-retirement.local (add to /etc/hosts if needed)"
echo ""
echo "To view logs:"
echo "  kubectl logs -f deployment/crypto-retirement-web -n crypto-retirement"
echo ""
echo "To access shell:"
echo "  kubectl exec -it deployment/crypto-retirement-web -n crypto-retirement -- sh"