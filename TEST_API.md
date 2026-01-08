# 🧪 Testing Your API

## ✅ Your Server is Running!

Your API server is running on **http://127.0.0.1:8000** (or http://localhost:8000)

---

## 🌐 How to Access

### Option 1: Use `localhost` instead of `0.0.0.0`
In your browser, go to:
- **http://localhost:8000**
- **http://localhost:8000/docs** (API Documentation - Interactive!)
- **http://localhost:8000/health** (Health Check)

### Option 2: Use `127.0.0.1`
- **http://127.0.0.1:8000**
- **http://127.0.0.1:8000/docs**

---

## 📚 Quick Test Endpoints

### 1. Health Check
Open in browser:
```
http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "statistics": {...}
}
```

### 2. Root Endpoint
```
http://localhost:8000/
```

### 3. API Documentation (Swagger UI)
```
http://localhost:8000/docs
```
**This is the best way to test!** You'll see an interactive interface where you can:
- See all endpoints
- Test API calls
- View request/response schemas

---

## 🧪 Test with curl (Command Line)

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Statistics
```bash
curl http://localhost:8000/api/v1/statistics
```

### Get All Products
```bash
curl http://localhost:8000/api/v1/products
```

### Create a Product
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Test Product\", \"issuer\": \"Test Bank\"}"
```

---

## 🐛 Troubleshooting

### If "Site Can't Be Reached"

1. **Check the server is running:**
   - You should see: "Uvicorn running on http://127.0.0.1:8000"
   - Don't use `0.0.0.0` in browser

2. **Use correct URL:**
   - ✅ Use: `http://localhost:8000`
   - ✅ Use: `http://127.0.0.1:8000`
   - ❌ Don't use: `http://0.0.0.0:8000`

3. **Check firewall:**
   - Windows Firewall might block it
   - Try disabling temporarily to test

4. **Check port is free:**
   - Make sure nothing else is using port 8000

---

## ✅ Success Indicators

When working correctly, you should see:

1. **In Terminal:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

2. **In Browser (http://localhost:8000/docs):**
   - Beautiful Swagger UI interface
   - List of all API endpoints
   - Interactive testing interface

---

## 🎯 Next Steps

1. Open **http://localhost:8000/docs** in your browser
2. Try the `/health` endpoint first
3. Try creating a product
4. Explore all available endpoints

**Your API is ready to use! 🚀**
