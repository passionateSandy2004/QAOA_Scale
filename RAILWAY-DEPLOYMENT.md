# 🚂 Deploy QAOA Portfolio Optimizer to Railway

Railway is perfect for your QAOA optimizer - **no sleep policy**, fast builds, and Docker support!

## 🏆 **Why Railway is Perfect:**
- ✅ **512MB RAM** - Perfect for quantum computing
- ✅ **No sleep policy** - Always available 24/7
- ✅ **Fast Docker builds** - Uses your Dockerfile.prod
- ✅ **Free HTTPS** - Secure by default
- ✅ **Git-based deployment** - Push to deploy
- ✅ **100GB bandwidth/month** - Generous limits

## 🚀 **Step-by-Step Deployment**

### **Step 1: Prepare Your Repository**

Make sure you have these files (already created):
- ✅ `Dockerfile.prod` - Production Docker image
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - With Gunicorn
- ✅ `api.py` - Your Flask application

### **Step 2: Push to GitHub**

```bash
# Add all files to git
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### **Step 3: Deploy to Railway**

1. **Go to Railway**
   - Visit: [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Sign up with GitHub

2. **Create New Project**
   - Click "Deploy from GitHub repo"
   - Select your QAOA repository
   - Railway will automatically detect your Dockerfile

3. **Configuration (Automatic)**
   - Railway reads `railway.json`
   - Uses `Dockerfile.prod`
   - Sets up health checks at `/health`

### **Step 4: Environment Variables**

In Railway dashboard → Variables tab, add:
```
PORT=8000
FLASK_ENV=production
PYTHONUNBUFFERED=1
```

### **Step 5: Deploy & Test**

Railway will automatically build and deploy. You'll get a URL like:
```
https://qaoa-portfolio-optimizer-production.railway.app
```

## 🧪 **Test Your Deployment**

```bash
# Replace with your Railway URL
export RAILWAY_URL="https://your-app.railway.app"

# Test health endpoint
curl $RAILWAY_URL/health

# Test optimization (with small parameters for free tier)
curl -X POST $RAILWAY_URL/optimize/today \
  -F "file=@sample_stock_data.csv" \
  -F "budget=3" \
  -F "depth=1" \
  -F "grid=2" \
  -F "shots=50"
```

## 📊 **Expected Response**

**Health Check:**
```json
{
  "status": "healthy",
  "service": "QAOA Portfolio Optimizer"
}
```

**Optimization Result:**
```json
{
  "picks": ["STOCK_01", "STOCK_03", "STOCK_05"],
  "filename": "sample_stock_data.csv",
  "parameters": {
    "budget": 3,
    "depth": 1,
    "grid": 2,
    "shots": 50
  }
}
```

## 🎯 **Railway-Specific Optimizations**

### **1. Resource Limits for Free Tier**

Your current `Dockerfile.prod` is already optimized:
- **2 Gunicorn workers** (instead of 4)
- **120s timeout** for quantum computations
- **Non-root user** for security

### **2. Recommended Parameters**

For Railway's free tier, use these parameters:
- **Budget**: 3-5 stocks
- **Depth**: 1-2 (QAOA circuit depth)
- **Grid**: 2-3 (parameter search)
- **Shots**: 50-100 (quantum simulations)

### **3. Custom Domain (Optional)**

In Railway dashboard:
1. Go to Settings → Domains
2. Add your custom domain
3. Railway provides free SSL certificates

## 📈 **Monitoring Your App**

### **Railway Dashboard**
- **Logs**: Real-time application logs
- **Metrics**: CPU, RAM, and network usage
- **Deployments**: Build history and status

### **Health Monitoring**
```bash
# Check if your app is healthy
curl https://your-app.railway.app/health

# Monitor response time
curl -w "@curl-format.txt" -o /dev/null -s https://your-app.railway.app/health
```

Create `curl-format.txt`:
```
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

## 🔧 **Troubleshooting**

### **Build Fails**
```bash
# Check Railway logs in dashboard
# Common issue: Missing railway.json

# Ensure railway.json exists:
cat railway.json
```

### **App Crashes**
```bash
# Check Railway logs for errors
# Common issue: Memory limits

# Reduce Gunicorn workers if needed
# Edit Dockerfile.prod: --workers 1
```

### **Slow Response**
```bash
# Quantum computation is CPU intensive
# Reduce parameters:
# - shots: 25-50
# - grid: 2
# - depth: 1
```

### **File Upload Issues**
```bash
# Check file size (Railway limit: ~25MB)
# Check CSV format
# Ensure proper headers: Content-Type: multipart/form-data
```

## 💰 **Railway Free Tier Limits**

- **512MB RAM** - Perfect for your app
- **Shared CPU** - 0.5 CPU cores
- **1GB Storage** - For your Docker image
- **100GB Bandwidth/month** - Very generous
- **No sleep policy** - Always available!

## 🆙 **When to Upgrade**

Consider Railway Pro ($5/month) when you need:
- **1GB+ RAM** for larger datasets
- **More CPU** for complex optimizations
- **Priority support**
- **Team collaboration**

## 🎉 **You're Live!**

Once deployed on Railway, your QAOA Portfolio Optimizer will be:
- 🌍 **Accessible worldwide**
- 🔒 **HTTPS secured**
- ⚡ **Always available**
- 📊 **Production ready**

Share your Railway URL with anyone to use your quantum portfolio optimizer! 🚀

## 📞 **Need Help?**

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Community support
- **Your Logs**: Railway dashboard → Logs tab

Your quantum portfolio optimizer is now ready for the world! 🌟