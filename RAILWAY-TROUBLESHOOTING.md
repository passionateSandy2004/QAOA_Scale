# 🔧 Railway Deployment Troubleshooting

Your Railway deployment is failing at the healthcheck stage. Here are multiple solutions to try:

## 🚨 **Current Issue**
```
Attempt #1 failed with service unavailable. Continuing to retry for 4m49s
```

This means Railway can build your app but it's not responding to the `/health` endpoint.

## 🛠️ **Solution 1: Use Simpler Configuration (RECOMMENDED)**

Replace your current `railway.json` with the simpler version:

```bash
# Backup current config
cp railway.json railway.json.backup

# Use the simpler config
cp railway-simple.json railway.json
```

This lets Railway auto-detect your Python app instead of using Docker.

## 🛠️ **Solution 2: Use Procfile (Alternative)**

Railway can auto-detect apps with a `Procfile`:

1. **Delete or rename railway.json**:
   ```bash
   mv railway.json railway.json.disabled
   ```

2. **Use the Procfile** (already created):
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api:create_app()
   ```

3. **Commit and deploy**:
   ```bash
   git add Procfile
   git commit -m "Use Procfile for Railway deployment"
   git push origin main
   ```

## 🛠️ **Solution 3: Debug with Startup Script**

Use the enhanced Dockerfile with logging:

1. **Check the startup script** (`start.sh`) - already created
2. **Commit the changes**:
   ```bash
   git add start.sh Dockerfile.railway
   git commit -m "Add startup script with logging"
   git push origin main
   ```

3. **Check Railway logs** for detailed output

## 🔍 **Debugging Steps**

### **1. Check Railway Logs**
In Railway dashboard:
- Go to your project
- Click "Logs" tab
- Look for errors during startup

### **2. Common Issues & Solutions**

#### **Port Binding Issue**
```bash
# Problem: App not binding to correct port
# Solution: Ensure $PORT is used correctly
```

#### **Import Error**
```bash
# Problem: Python modules not found
# Solution: Check requirements.txt includes all dependencies
```

#### **Memory Limit**
```bash
# Problem: App crashes due to memory
# Solution: Reduce workers to 1
```

#### **Timeout Issue**
```bash
# Problem: App takes too long to start
# Solution: Increase healthcheck timeout
```

## 🚀 **Quick Fix Commands**

### **Option A: Simple Auto-Detection**
```bash
# Use Railway's auto-detection
mv railway.json railway.json.disabled
git add .
git commit -m "Let Railway auto-detect app"
git push origin main
```

### **Option B: Use Procfile**
```bash
# Use Procfile approach
mv railway.json railway.json.disabled
git add Procfile
git commit -m "Use Procfile for deployment"
git push origin main
```

### **Option C: Minimal Docker**
```bash
# Use minimal railway config
cp railway-simple.json railway.json
git add railway.json
git commit -m "Use minimal Railway config"
git push origin main
```

## 📊 **Expected Working Output**

Once working, you should see:
```
✅ Build successful
✅ Healthcheck passing at /health
✅ Deployment successful
✅ Service available at: https://your-app.railway.app
```

## 🧪 **Test Your Deployment**

```bash
# Replace with your Railway URL
export RAILWAY_URL="https://your-app.railway.app"

# Test health
curl $RAILWAY_URL/health

# Expected response:
{"status": "healthy", "service": "QAOA Portfolio Optimizer"}
```

## 💡 **Railway-Specific Tips**

1. **Start Simple**: Let Railway auto-detect first
2. **Use Procfile**: Simpler than Docker for many cases
3. **Check Logs**: Always check deployment logs for errors
4. **Resource Limits**: Railway free tier has 512MB RAM limit
5. **Patience**: First deployment can take 5-10 minutes

## 🔄 **Recovery Steps**

If all else fails:
1. **Delete the project** in Railway dashboard
2. **Create a new project**
3. **Use the Procfile approach** (simplest)
4. **Deploy fresh**

Try **Option A** first (auto-detection) - it's the most reliable for Railway! 🚂