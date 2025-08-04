# OpenLDAP FastAPI Authentication System

A complete authentication system built with OpenLDAP, FastAPI, React, and MongoDB.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Run the Application

```bash
# Clone and navigate to the project
cd openldab_fastapi

# Start all services
docker-compose up -d

# Verify everything is running
docker-compose ps
```

That's it! The application will be available at:
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🔐 Default Login Credentials

### Admin User
- **Username:** `user1`
- **Password:** `password123`
- **Access:** Admin Dashboard

### Regular User
- **Username:** `user2` 
- **Password:** `password123`
- **Access:** User Dashboard

## 🛠️ Development Commands

```bash
# Stop all services
docker compose down

# View logs
docker compose logs

# Restart with rebuild
docker compose up -d --build

# Clean restart (removes data)
docker compose down -v && docker compose up -d
```

## 🏗️ Architecture

- **Authentication:** OpenLDAP with custom schema
- **Backend API:** FastAPI with async operations
- **Frontend:** React with modern UI components
- **Database:** MongoDB for application data
- **Container Orchestration:** Docker Compose
- **User Management:** phpLDAPadmin interface

## 🚨 Troubleshooting

If you encounter issues:

1. **Check service status:**
   ```bash
   docker-compose ps
   ```

2. **View service logs:**
   ```bash
   docker-compose logs openldap
   docker-compose logs fastapi_backend
   ```

3. **Clean restart:**
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

4. **Port conflicts:** Ensure ports 3000, 8000, 1389, 8080, and 27017 are available
