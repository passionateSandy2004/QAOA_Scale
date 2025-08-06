# 🚀 Free Deployment Options for QAOA Portfolio Optimizer

Deploy your QAOA Portfolio Optimizer to the cloud for **FREE** using these platforms! Each has different features and limits.

## 📊 **Platform Comparison**

| Platform | CPU/RAM | Storage | Bandwidth | Build Time | Sleep Policy | Best For |
|----------|---------|---------|-----------|------------|--------------|----------|
| **Railway** | 0.5 CPU, 512MB | 1GB | 100GB/month | ✅ Fast | Never sleeps | **RECOMMENDED** |
| **Render** | 0.1 CPU, 512MB | 1GB | 100GB/month | ⚠️ Slow | Sleeps after 15min | Simple setup |
| **Fly.io** | Shared CPU, 256MB | 3GB | 160GB/month | ✅ Fast | Never sleeps | Developer-friendly |
| **Heroku** | 1 CPU, 512MB | - | 550 hours/month | ✅ Fast | Sleeps after 30min | Enterprise-grade |

## 🏆 **RECOMMENDED: Railway (Best Overall)**

Railway offers the best free tier for containerized apps like yours.

### **✅ Why Railway:**
- **No sleep policy** - Always available
- **Fast builds** - Docker support
- **512MB RAM** - Sufficient for QAOA
- **Simple deployment** - Git-based
- **Custom domains** - Free HTTPS

### **🚀 Deploy to Railway:**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Prepare Your Repository**
   ```bash
   # Create railway.json for configuration
   echo '{
     "build": {
       "builder": "dockerfile",
       "dockerfilePath": "Dockerfile.prod"
     },
     "deploy": {
       "restartPolicyType": "always"
     }
   }' > railway.json
   
   # Push to GitHub
   git add .
   git commit -m "Add Railway configuration"
   git push origin main
   ```

3. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Dockerfile and deploys

4. **Configure Environment**
   - In Railway dashboard: Variables tab
   - Add: `PORT=8000`
   - Add: `FLASK_ENV=production`

5. **Get Your URL**
   - Railway provides: `https://your-app-name.railway.app`
   - Test: `curl https://your-app-name.railway.app/health`

---

## 🎨 **Alternative: Render (Easiest Setup)**

Great for beginners with simple Git-based deployment.

### **🚀 Deploy to Render:**

1. **Create render.yaml**
   ```yaml
   services:
     - type: web
       name: qaoa-optimizer
       env: docker
       dockerfilePath: ./Dockerfile.prod
       plan: free
       envVars:
         - key: FLASK_ENV
           value: production
         - key: PORT
           value: 8000
   ```

2. **Deploy Steps**
   - Go to [render.com](https://render.com)
   - Connect GitHub repository
   - Render auto-deploys from render.yaml

3. **⚠️ Limitations**
   - **Sleeps after 15 minutes** of inactivity
   - **Slow cold starts** (30+ seconds)
   - **Limited CPU** (0.1 CPU units)

---

## ⚡ **Alternative: Fly.io (Developer-Friendly)**

Great performance with Docker-native deployment.

### **🚀 Deploy to Fly.io:**

1. **Install Fly CLI**
   ```bash
   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml**
   ```toml
   app = "qaoa-optimizer"
   primary_region = "iad"
   
   [build]
     dockerfile = "Dockerfile.prod"
   
   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = false
     auto_start_machines = true
     min_machines_running = 1
   
   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   ```

3. **Deploy**
   ```bash
   fly auth login
   fly launch --no-deploy
   fly deploy
   ```

4. **Get URL**
   ```bash
   fly open
   # Or: https://qaoa-optimizer.fly.dev
   ```

---

## 🏢 **Alternative: Heroku (Enterprise-Grade)**

Most mature platform with excellent documentation.

### **🚀 Deploy to Heroku:**

1. **Create heroku.yml**
   ```yaml
   build:
     docker:
       web: Dockerfile.prod
   run:
     web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 api:create_app()
   ```

2. **Deploy Steps**
   ```bash
   # Install Heroku CLI
   # Windows: Download from heroku.com/cli
   
   heroku login
   heroku create qaoa-optimizer-your-name
   heroku stack:set container
   git push heroku main
   ```

3. **⚠️ Limitations**
   - **Sleeps after 30 minutes** of inactivity
   - **550 hours/month** limit
   - **Dyno cycling** every 24 hours

---

## 🛠️ **Deployment Preparation**

### **1. Create Deployment-Ready Files**

Create these files in your project root:

**railway.json** (for Railway):
```json
{
  "build": {
    "builder": "dockerfile",
    "dockerfilePath": "Dockerfile.prod"
  },
  "deploy": {
    "restartPolicyType": "always"
  }
}
```

**render.yaml** (for Render):
```yaml
services:
  - type: web
    name: qaoa-optimizer
    env: docker
    dockerfilePath: ./Dockerfile.prod
    plan: free
    envVars:
      - key: FLASK_ENV
        value: production
```

**fly.toml** (for Fly.io):
```toml
app = "qaoa-optimizer"

[build]
  dockerfile = "Dockerfile.prod"

[http_service]
  internal_port = 8000
  force_https = true
```

### **2. Optimize for Free Tiers**

Update `Dockerfile.prod` for resource constraints:

```dockerfile
# Reduce workers for free tiers
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "api:create_app()"]
```

### **3. Test Locally**
```bash
# Test production build
docker build -f Dockerfile.prod -t qaoa-test .
docker run -p 8000:8000 qaoa-test

# Test endpoints
curl http://localhost:8000/health
```

## 🎯 **Deployment Commands Summary**

```bash
# Railway (Recommended)
git push origin main  # Auto-deploys

# Render
git push origin main  # Auto-deploys

# Fly.io
fly deploy

# Heroku
git push heroku main
```

## 📝 **Post-Deployment Testing**

```bash
# Test your deployed API
curl https://your-app.railway.app/health

# Test optimization (replace URL)
curl -X POST https://your-app.railway.app/optimize/today \
  -F "file=@sample_stock_data.csv" \
  -F "budget=3" \
  -F "depth=1" \
  -F "grid=2" \
  -F "shots=50"
```

## 💡 **Pro Tips**

1. **Use Railway** for best performance and reliability
2. **Keep optimization parameters low** on free tiers:
   - budget: 3-5
   - depth: 1-2  
   - grid: 2-3
   - shots: 50-100

3. **Monitor usage** to stay within free limits
4. **Use custom domains** for professional URLs
5. **Set up monitoring** for uptime tracking

## 🆙 **Upgrade Options**

When you outgrow free tiers:
- **Railway Pro**: $5/month, better resources
- **Render Starter**: $7/month, no sleep
- **Fly.io Scale**: Pay-as-you-use
- **Heroku Hobby**: $7/month, no sleep

Your QAOA optimizer is now ready for the world! 🌍🚀