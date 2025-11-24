# 🚀 Guide Déploiement Production

> Guide complet pour déployer MicroFrame en production avec Docker, Nginx et best practices

## 📋 Prérequis

- Application MicroFrame fonctionnelle
- Docker installé (optionnel)
- Serveur Linux (Ubuntu/Debian recommandé)
- Nom de domaine configuré

---

## 🐳 Déploiement avec Docker

### 1. Dockerfile

Créez `Dockerfile` :

```dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Requirements.txt

```txt
microframe>=2.0.0
uvicorn[standard]>=0.24.0
python-jose[cryptography]
bcrypt
python-multipart
```

### 3. Docker Compose

Créez `docker-compose.yml` :

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - DEBUG=false
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    restart: unless-stopped
```

### 4. Build et Run

```bash
# Build l'image
docker-compose build

# Lancer
docker-compose up -d

# Voir les logs
docker-compose logs -f app

# Stop
docker-compose down
```

---

## 🌐 Configuration Nginx

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    
    server {
        listen 80;
        server_name votre-domaine.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name votre-domaine.com;
        
        # SSL certificates
        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;
        
        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        
        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        
        # Proxy settings
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Rate limiting
            limit_req zone=api_limit burst=20 nodelay;
        }
        
        # WebSocket support
        location /ws/ {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 86400;
        }
        
        # Static files (si applicable)
        location /static/ {
            alias /app/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

---

## ⚙️ Configuration Production

### .env Production

```bash
# Application
DEBUG=false
APP_ENV=production
SECRET_KEY=votre-cle-generee-securisee-64-caracteres
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Database
DATABASE_URL=postgresql://user:password@db:5432/myapp

# AuthX
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com

# Security
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Monitoring
SENTRY_DSN=https://...
LOG_LEVEL=INFO
```

### Configuration App

```python
# config.py
import os
from microframe import AppConfig
from microframe.authx import AuthConfig

# App config
app_config = AppConfig(
    title="Mon API",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true",
    docs_url="/docs" if os.getenv("DEBUG") == "true" else None,  # Désactiver en prod
    redoc_url=None,
    openapi_url=None
)

# Auth config
auth_config = AuthConfig(
    secret_key=os.getenv("SECRET_KEY"),
    algorithm="HS256",
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)),
    refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
)

# Validation
assert app_config.debug is False, "DEBUG should be False in production"
assert auth_config.secret_key, "SECRET_KEY must be set"
assert len(auth_config.secret_key) >= 32, "SECRET_KEY too short"
```

---

## 🔒 SSL/TLS avec Let's Encrypt

### Installation Certbot

```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obtenir certificat
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Auto-renewal (déjà configuré par défaut)
sudo systemctl status certbot.timer
```

### Renouvellement Manuel

```bash
# Tester le renouvellement
sudo certbot renew --dry-run

# Renouveler
sudo certbot renew
```

---

## 🏃 Uvicorn Production

### Configuration Optimale

```bash
# Avec workers multiples (CPU cores * 2 + 1)
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level warning \
  --access-log \
  --proxy-headers \
  --forwarded-allow-ips='*'
```

### Avec Gunicorn (Recommandé)

```bash
# Install
pip install gunicorn

# Run
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level warning \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

---

## 🗄️ Base de Données

### PostgreSQL avec Docker

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: myapp_prod
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Migrations (avec Alembic)

```bash
# Install
pip install alembic

# Init
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply
alembic upgrade head
```

---

## 📊 Monitoring

### Logging

```python
# app.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)

log_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger = logging.getLogger('microframe')
logger.addHandler(log_handler)
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)
```

### Health Check

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
```

### Prometheus Metrics (Optionnel)

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")
```

---

## 🔐 Sécurité Production

### Checklist Sécurité

- ✅ HTTPS obligatoire (Let's Encrypt)
- ✅ Security headers (Nginx)
- ✅ Rate limiting activé
- ✅ CORS configuré strictement
- ✅ DEBUG=false
- ✅ Docs désactivées (`docs_url=None`)
- ✅ Secret key fort (64+ caractères)
- ✅ Dépendances à jour
- ✅ Firewall configuré
- ✅ SSH key-based auth only

### Firewall (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow OpenSSH

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

---

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml avec scaling
services:
  app:
    build: .
    deploy:
      replicas: 4
    environment:
      - SECRET_KEY=${SECRET_KEY}
```

```bash
# Scale up/down
docker-compose up -d --scale app=6
```

### Load Balancing (Nginx)

```nginx
upstream app_servers {
    least_conn;  # Load balancing method
    server app1:8000;
    server app2:8000;
    server app3:8000;
    server app4:8000;
}

server {
    location / {
        proxy_pass http://app_servers;
    }
}
```

---

## 🚀 Déploiement Continu (CI/CD)

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t myapp:latest .
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push myapp:latest
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
            docker-compose logs -f --tail=50
```

---

## 🔄 Backup

### Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup PostgreSQL
docker exec microframe_db pg_dump -U myapp myapp_prod > "$BACKUP_DIR/db_$DATE.sql"

# Compress
gzip "$BACKUP_DIR/db_$DATE.sql"

# Keep last 7 days
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +7 -delete
```

### Cron Job

```bash
# Edit crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## 📝 Checklist Déploiement

### Avant le Déploiement

- [ ] Tests passent tous
- [ ] Configuration production validée
- [ ] Secrets sécurisés (.env)
- [ ] SSL/TLS configuré
- [ ] Database migrations prêtes
- [ ] Backup strategy en place
- [ ] Monitoring configuré
- [ ] Documentation à jour

### Après le Déploiement

- [ ] Health check OK
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] Performance testée (load testing)
- [ ] SSL vérifié (https://www.ssllabs.com/)
- [ ] Security headers vérifiés
- [ ] Backup testé (restore)

---

## 📖 Ressources

- **[Best Practices](best-practices.md)** - Optimisations et sécurité
- **[Nginx Docs](https://nginx.org/en/docs/)** - Documentation Nginx
- **[Docker Docs](https://docs.docker.com/)** - Documentation Docker

---

---

## 📖 Navigation

**Parcours Documentation** :
1. [Index](../README.md)
2. [Getting Started](getting-started.md)
3. [Authentication](authentication.md)
4. [WebSocket Chat](websocket-chat.md)
5. **📍 Deployment** (vous êtes ici)
6. [Best Practices](best-practices.md)

---

**[← WebSocket Chat](websocket-chat.md)** | **[Index](../README.md)** | **[Best Practices →](best-practices.md)**
