#!/bin/bash
# Docker startup script for VERITAS Command Center

echo "========================================="
echo "  VERITAS Command Center - Docker Setup"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "   Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "   Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Build and start containers
echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "========================================="
echo "  Services Starting..."
echo "========================================="
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check service health
echo ""
echo "Checking service status..."
docker-compose ps

echo ""
echo "========================================="
echo "  ✅ VERITAS Command Center is running!"
echo "========================================="
echo ""
echo "📍 Access points:"
echo "   API:        http://localhost:8000/docs"
echo "   Dashboard:  http://localhost:8501"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop:         docker-compose down"
echo "   Restart:      docker-compose restart"
echo "   Status:       docker-compose ps"
echo ""
