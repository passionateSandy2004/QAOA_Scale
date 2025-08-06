# QAOA Portfolio Optimizer - Production Deployment Guide

This guide covers deploying the QAOA Portfolio Optimizer API in a production environment using Docker.

## 🏭 Production vs Development

| Feature | Development | Production |
|---------|-------------|------------|
| **Server** | Flask dev server | Gunicorn WSGI |
| **Port** | 9000 | 8000 (behind Nginx on 80/443) |
| **Workers** | 1 | 4 Gunicorn workers |
| **Reverse Proxy** | None | Nginx |
| **Rate Limiting** | None | Yes (10 req/s general, 2 req/s uploads) |
| **SSL** | No | Optional (configured) |
| **Resource Limits** | None | CPU: 2 cores, RAM: 4GB |
| **Logging** | Console | Structured JSON logs |
| **Health Checks** | Basic | Advanced with retries |

## 🚀 Quick Production Deployment

### 1. Build and Run Production Stack

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up --build -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 2. Test Production Deployment

```bash
# Health check
curl http://localhost/health

# Test optimization endpoint
curl -X POST http://localhost/optimize/today \
  -F "file=@your_data.csv" \
  -F "budget=5" \
  -F "depth=2" \
  -F "grid=3" \
  -F "shots=100"
```

## 📁 Production File Structure

```
.
├── Dockerfile.prod              # Production Dockerfile
├── docker-compose.prod.yml      # Production compose configuration
├── nginx.conf                   # Nginx reverse proxy config
├── api.py                       # Flask application
├── portfolio_optimizer/         # Core optimization package
├── requirements.txt             # Python dependencies (includes Gunicorn)
└── ssl/                        # SSL certificates (optional)
    ├── cert.pem
    └── key.pem
```

## 🔧 Production Configuration Details

### Gunicorn WSGI Server
- **Workers**: 4 processes
- **Timeout**: 120 seconds (for quantum computations)
- **Keep-alive**: 2 seconds
- **Max requests**: 1000 per worker (prevents memory leaks)
- **Binding**: 0.0.0.0:8000

### Nginx Reverse Proxy
- **Rate limiting**: 10 req/s general, 2 req/s for uploads
- **File upload limit**: 20MB
- **Gzip compression**: Enabled
- **Security headers**: Added
- **Timeouts**: 5 minutes for optimization requests

### Resource Limits
- **CPU**: 2 cores max, 0.5 cores reserved
- **Memory**: 4GB max, 1GB reserved
- **Log rotation**: 10MB max, 3 files

## 🛡️ Security Features

### 1. Application Security
- Non-root user (UID 1000)
- Read-only file mounts
- Temporary file cleanup
- Input validation

### 2. Network Security
- Rate limiting (prevents abuse)
- Security headers
- CORS protection
- Request size limits

### 3. Infrastructure Security
- Container isolation
- Network segmentation
- Health monitoring
- Log management

## 🌐 Domain and SSL Setup

### 1. Domain Configuration

Update `nginx.conf` for your domain:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of config
}
```

### 2. SSL Certificate Setup

#### Option A: Let's Encrypt (Free)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Copy certificates to ssl/ directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

#### Option B: Self-signed (Development)
```bash
mkdir ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

## 📊 Monitoring and Logging

### 1. Check Service Health
```bash
# Container status
docker-compose -f docker-compose.prod.yml ps

# Resource usage
docker stats

# Health endpoint
curl http://localhost/health
```

### 2. View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs qaoa-api
docker-compose -f docker-compose.prod.yml logs nginx

# Follow logs
docker-compose -f docker-compose.prod.yml logs -f --tail=100
```

### 3. Performance Monitoring
```bash
# API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost/health

# Create curl-format.txt:
echo "     time_namelookup:  %{time_namelookup}\n\
        time_connect:  %{time_connect}\n\
     time_appconnect:  %{time_appconnect}\n\
    time_pretransfer:  %{time_pretransfer}\n\
       time_redirect:  %{time_redirect}\n\
  time_starttransfer:  %{time_starttransfer}\n\
                     ----------\n\
          time_total:  %{time_total}\n" > curl-format.txt
```

## 🔄 Scaling and Load Balancing

### 1. Horizontal Scaling
```yaml
# In docker-compose.prod.yml
services:
  qaoa-api:
    deploy:
      replicas: 3  # Run 3 instances
```

### 2. Load Balancer Configuration
```nginx
# In nginx.conf
upstream qaoa_backend {
    server qaoa-api_1:8000;
    server qaoa-api_2:8000;
    server qaoa-api_3:8000;
    keepalive 32;
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check what's using port 80
   sudo lsof -i :80
   ```

2. **Permission issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod +x nginx.conf
   ```

3. **Memory issues**
   ```bash
   # Monitor memory usage
   docker stats
   
   # Reduce workers if needed
   # Edit Dockerfile.prod: --workers 2
   ```

4. **SSL certificate issues**
   ```bash
   # Test SSL configuration
   openssl s_client -connect localhost:443 -servername your-domain.com
   ```

### Log Analysis
```bash
# Find errors in logs
docker-compose -f docker-compose.prod.yml logs | grep ERROR

# Check Nginx access patterns
docker-compose -f docker-compose.prod.yml logs nginx | grep "POST /optimize"

# Monitor rate limiting
docker-compose -f docker-compose.prod.yml logs nginx | grep "429"
```

## 🔧 Environment-Specific Configuration

### Staging Environment
```bash
# Copy production config
cp docker-compose.prod.yml docker-compose.staging.yml

# Modify for staging (reduced resources, different ports)
# Edit docker-compose.staging.yml
```

### Cloud Deployment (AWS/GCP/Azure)

1. **Use managed container services**:
   - AWS ECS/Fargate
   - Google Cloud Run
   - Azure Container Instances

2. **External load balancer**:
   - AWS ALB
   - GCP Load Balancer
   - Azure Load Balancer

3. **Managed databases** (if needed):
   - AWS RDS
   - Google Cloud SQL
   - Azure Database

## 🏁 Production Checklist

- [ ] SSL certificates configured
- [ ] Domain name pointing to server
- [ ] Firewall rules configured (80, 443)
- [ ] Log rotation set up
- [ ] Monitoring alerts configured
- [ ] Backup strategy implemented
- [ ] Resource limits tested
- [ ] Rate limiting tested
- [ ] Health checks working
- [ ] Error handling tested

## 📞 Support

For production issues:
1. Check logs first: `docker-compose -f docker-compose.prod.yml logs`
2. Verify health endpoint: `curl http://localhost/health`
3. Check resource usage: `docker stats`
4. Review Nginx configuration: `nginx -t`

Remember: Production deployment requires careful monitoring and regular maintenance!