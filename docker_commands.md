# Docker Commands for Label Studio

## Prerequisites
- Docker Desktop installed and running on Windows
- Ensure Docker Desktop is started before running these commands

## Quick Start (Using Docker Compose - Recommended)

```bash
# Navigate to project directory
cd te-aihub-intern-assignment-arun-kumar

# Start Label Studio
docker-compose up -d

# View logs
docker-compose logs -f

# Stop Label Studio
docker-compose down
```

## Manual Docker Commands

### Pull Label Studio Image
```bash
docker pull heartexlabs/label-studio:latest
```

### Run Label Studio Container
```bash
docker run -d -p 8080:8080 \
  -v label-studio-data:/label-studio/data \
  --name label-studio \
  heartexlabs/label-studio:latest
```

### Alternative: Run with Local Data Persistence
```bash
docker run -d -p 8080:8080 \
  -v "$(pwd)/mydata:/label-studio/data" \
  --name label-studio \
  heartexlabs/label-studio:latest
```

### For Windows PowerShell
```powershell
docker run -d -p 8080:8080 `
  -v label-studio-data:/label-studio/data `
  --name label-studio `
  heartexlabs/label-studio:latest
```

## Useful Commands

### Check if container is running
```bash
docker ps
```

### View container logs
```bash
docker logs label-studio
```

### Stop the container
```bash
docker stop label-studio
```

### Remove the container
```bash
docker rm label-studio
```

### Restart the container
```bash
docker start label-studio
```

## Access Label Studio
Once running, open your browser and go to:
**http://localhost:8080**

## First-time Setup
1. Create an account (local account, no email verification needed)
2. Create a new project named "BCCD Annotation Assignment"
3. Import images and configure labels
