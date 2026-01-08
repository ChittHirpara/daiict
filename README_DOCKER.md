# 🐳 Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker Desktop installed ([Download](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

### Option 1: Quick Start (Recommended)

**Windows:**
```batch
docker-start.bat
```

**Mac/Linux:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Option 2: Manual Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## What Gets Deployed

1. **API Server** (Port 8000)
   - FastAPI backend
   - REST endpoints
   - WebSocket support

2. **Dashboard** (Port 8501)
   - Streamlit command center UI
   - Real-time monitoring

3. **Database** (Optional PostgreSQL)
   - Currently uses SQLite (file-based)
   - Can enable PostgreSQL in `docker-compose.yml`

---

## Access Points

After starting:
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

---

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild (after code changes)
docker-compose up -d --build

# Check status
docker-compose ps
```

---

## Production Deployment

For production, modify `docker-compose.yml` to:
1. Enable PostgreSQL database
2. Add environment variables
3. Configure volumes for data persistence
4. Set up reverse proxy (nginx)
5. Enable SSL/TLS

---

## Troubleshooting

**Ports already in use:**
- Change ports in `docker-compose.yml`

**Build fails:**
- Check internet connection (downloads models)
- Increase Docker memory limit

**Services not starting:**
- Check logs: `docker-compose logs`
- Verify Docker has enough resources

---

## Development Mode

For development with live code reload:
```bash
docker-compose up
```
Remove `-d` flag to see logs in terminal.
