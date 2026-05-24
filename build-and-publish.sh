#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AiFACTORi Docker Build & Publish Script
# Builds and publishes production containers to Docker Hub
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Configuration
REGISTRY="docker.io"
DOCKER_USERNAME="${DOCKER_USERNAME:-ladbotodelad}"
IMAGE_PREFIX="${DOCKER_USERNAME}"
VERSION="${VERSION:-2.0}"
LOCK_CYCLE="2"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  AiFACTORi Docker Build & Publish                             ║"
echo "║  Registry: $REGISTRY                                          ║"
echo "║  Username: $DOCKER_USERNAME                                   ║"
echo "║  Version: $VERSION (Cycle $LOCK_CYCLE)                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verify Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

# Verify logged in to Docker Hub
if ! docker info | grep -q "Username"; then
    echo "⚠️  Not logged in to Docker Hub. Running: docker login"
    docker login
fi

echo "🔨 Building AiFACTORi Engine Image..."
docker build \
    -f Dockerfile.aifactori \
    -t ${IMAGE_PREFIX}/aifactori-engine:${VERSION} \
    -t ${IMAGE_PREFIX}/aifactori-engine:latest \
    -t ${IMAGE_PREFIX}/aifactori-engine:cycle-${LOCK_CYCLE} \
    --build-arg VERSION=${VERSION} \
    --build-arg LOCK_CYCLE=${LOCK_CYCLE} \
    .

if [ $? -eq 0 ]; then
    echo "✅ AiFACTORi Engine image built successfully"
else
    echo "❌ Failed to build AiFACTORi Engine image"
    exit 1
fi

echo ""
echo "🔨 Building E14 Oracle Image..."
docker build \
    -f Dockerfile.e14-oracle \
    -t ${IMAGE_PREFIX}/e14-oracle:${VERSION} \
    -t ${IMAGE_PREFIX}/e14-oracle:latest \
    -t ${IMAGE_PREFIX}/e14-oracle:cycle-${LOCK_CYCLE} \
    --build-arg VERSION=${VERSION} \
    --build-arg LOCK_CYCLE=${LOCK_CYCLE} \
    .

if [ $? -eq 0 ]; then
    echo "✅ E14 Oracle image built successfully"
else
    echo "❌ Failed to build E14 Oracle image"
    exit 1
fi

echo ""
echo "📊 Images Ready for Push:"
docker images | grep -E "aifactori-engine|e14-oracle" || true

echo ""
read -p "Push images to Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📤 Pushing AiFACTORi Engine to Docker Hub..."
    docker push ${IMAGE_PREFIX}/aifactori-engine:${VERSION}
    docker push ${IMAGE_PREFIX}/aifactori-engine:latest
    docker push ${IMAGE_PREFIX}/aifactori-engine:cycle-${LOCK_CYCLE}
    
    if [ $? -eq 0 ]; then
        echo "✅ AiFACTORi Engine pushed successfully"
    else
        echo "❌ Failed to push AiFACTORi Engine"
        exit 1
    fi
    
    echo ""
    echo "📤 Pushing E14 Oracle to Docker Hub..."
    docker push ${IMAGE_PREFIX}/e14-oracle:${VERSION}
    docker push ${IMAGE_PREFIX}/e14-oracle:latest
    docker push ${IMAGE_PREFIX}/e14-oracle:cycle-${LOCK_CYCLE}
    
    if [ $? -eq 0 ]; then
        echo "✅ E14 Oracle pushed successfully"
    else
        echo "❌ Failed to push E14 Oracle"
        exit 1
    fi
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  ✅ All Images Published Successfully                         ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║                                                                ║"
    echo "║  AiFACTORi Engine:                                             ║"
    echo "║    docker pull ${IMAGE_PREFIX}/aifactori-engine:${VERSION}          ║"
    echo "║    docker pull ${IMAGE_PREFIX}/aifactori-engine:latest              ║"
    echo "║                                                                ║"
    echo "║  E14 Oracle:                                                   ║"
    echo "║    docker pull ${IMAGE_PREFIX}/e14-oracle:${VERSION}                ║"
    echo "║    docker pull ${IMAGE_PREFIX}/e14-oracle:latest                    ║"
    echo "║                                                                ║"
    echo "║  Run Deployment:                                               ║"
    echo "║    docker-compose -f docker-compose-e14-integration.yml up -d  ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
else
    echo "⏭️  Skipped push. Images ready locally."
    echo ""
    echo "To push manually:"
    echo "  docker push ${IMAGE_PREFIX}/aifactori-engine:${VERSION}"
    echo "  docker push ${IMAGE_PREFIX}/e14-oracle:${VERSION}"
fi

echo ""
echo "✅ Script completed successfully!"
