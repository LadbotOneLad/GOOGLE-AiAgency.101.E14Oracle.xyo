#!/bin/bash
# Production deployment helper for Codex 6.65
# Usage: ./deploy-production.sh <registry-url> <region> <scale>

set -e

REGISTRY="${1:-docker.io}"
REGION="${2:-us-east-1}"
SCALE="${3:-48}"  # 48, 128, or 256

echo "📦 Codex 6.65 Production Deployment"
echo "Registry: $REGISTRY"
echo "Region: $REGION"
echo "Scale: $SCALE engines"
echo ""

# Build and push
echo "🔨 Building image..."
docker buildx build --platform linux/amd64,linux/arm64 \
  -t $REGISTRY/codex665:latest \
  -t $REGISTRY/codex665:$(date +%Y%m%d-%H%M%S) \
  --push .

echo "✅ Image pushed"

# Update manifests
echo "📝 Updating manifests..."
sed -i "s|codex665:latest|$REGISTRY/codex665:latest|g" k8s-deployment.yaml
sed -i "s|replicas: 48|replicas: $SCALE|g" k8s-deployment.yaml
sed -i "s|maxReplicas: 256|maxReplicas: $((SCALE * 5))|g" k8s-deployment.yaml

# Apply to Kubernetes
echo "🚀 Deploying to Kubernetes..."
kubectl create namespace codex-6-65 --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-monitoring.yaml

# Wait for rollout
echo "⏳ Waiting for deployment..."
kubectl rollout status deployment/codex-engine -n codex-6-65 --timeout=10m

# Get service endpoints
echo ""
echo "✨ Deployment complete!"
echo ""
echo "Dashboard Access:"
kubectl get svc -n codex-6-65 | grep -E "prometheus|grafana|witness"

echo ""
echo "Next steps:"
echo "1. kubectl port-forward -n codex-6-65 svc/grafana 3000:3000"
echo "2. Open http://localhost:3000"
echo "3. Check logs: kubectl logs -f -n codex-6-65 -l app=codex-engine"
