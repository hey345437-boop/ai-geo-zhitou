#!/bin/bash

# 智投 - 一键启动脚本
# 此脚本用于设置和启动整个应用程序

set -e  # Exit on error

echo "=========================================="
echo "  智投 - 一键启动"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}Please edit .env file with your API keys before continuing${NC}"
    echo ""
    read -p "Press Enter to continue after editing .env, or Ctrl+C to exit..."
fi

echo ""
echo "Step 1: Stopping any existing containers..."
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Cleaned up existing containers${NC}"

echo ""
echo "Step 2: Building Docker images..."
docker-compose build
echo -e "${GREEN}✓ Docker images built${NC}"

echo ""
echo "Step 3: Starting services..."
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"

echo ""
echo "Step 4: Waiting for services to be ready..."
echo "  - Waiting for PostgreSQL..."
sleep 5
until docker-compose exec -T postgres pg_isready -U postgres &> /dev/null; do
    echo "    PostgreSQL is starting..."
    sleep 2
done
echo -e "${GREEN}  ✓ PostgreSQL is ready${NC}"

echo "  - Waiting for Redis..."
until docker-compose exec -T redis redis-cli ping &> /dev/null; do
    echo "    Redis is starting..."
    sleep 2
done
echo -e "${GREEN}  ✓ Redis is ready${NC}"

echo "  - Waiting for Backend API..."
sleep 5
until curl -s http://localhost:8000/health &> /dev/null; do
    echo "    Backend is starting..."
    sleep 2
done
echo -e "${GREEN}  ✓ Backend API is ready${NC}"

echo "  - Waiting for Frontend..."
sleep 3
until curl -s http://localhost:5173 &> /dev/null; do
    echo "    Frontend is starting..."
    sleep 2
done
echo -e "${GREEN}  ✓ Frontend is ready${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}  🎉 GEO Optimizer is now running!${NC}"
echo "=========================================="
echo ""
echo "Access the application:"
echo "  📱 Frontend:        http://localhost:5173"
echo "  🔧 Backend API:     http://localhost:8000"
echo "  📚 API Docs:        http://localhost:8000/docs"
echo "  🐰 RabbitMQ:        http://localhost:15672 (guest/guest)"
echo "  🔍 Neo4j Browser:   http://localhost:7474 (neo4j/password)"
echo ""
echo "Useful commands:"
echo "  View logs:          docker-compose logs -f"
echo "  Stop services:      docker-compose down"
echo "  Restart:            docker-compose restart"
echo ""
echo "Press Ctrl+C to stop viewing logs, services will continue running"
echo ""

# Follow logs
docker-compose logs -f
