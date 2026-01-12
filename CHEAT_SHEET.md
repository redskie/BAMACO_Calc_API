# ⚡ QUICK START CHEAT SHEET

## 🚀 Deploy API in 3 Steps

```bash
# 1. Push these files to GitHub:
git add api/ requirements.txt render.yaml
git commit -m "Add API backend"
git push

# 2. Go to render.com → New Web Service → Connect GitHub

# 3. Done! Your API is at: https://your-app.onrender.com
```

## 📦 Share with Clients in 2 Steps

```powershell
# 1. Create package
.\create-client-package.ps1

# 2. Share mai-tools-api-client.zip with developers
```

## 📋 Files Breakdown

### You Deploy (Backend)

- ✅ `api/app.py`
- ✅ `requirements.txt`
- ✅ `render.yaml`

### You Share (Clients)

- ✅ `API_DOCUMENTATION.md`
- ✅ `API_QUICK_REFERENCE.md`
- ✅ `API_INTEGRATION_ARCHITECTURE.md`
- ✅ `api_demo.html`
- ✅ Your API URL

### You Keep (Internal)

- 📝 `test_api.py`
- 📝 `test_api_edge_cases.py`
- 📝 `TEST_REPORT.md`

## 🔗 API Endpoints

```
GET  /health                → Health check
GET  /ranks                 → All rank definitions
POST /rating                → Calculate rating
POST /rating-range          → Min/max for rank
POST /recommended-levels    → Chart recommendations
```

## ✅ Test Commands

```bash
# Test locally
uvicorn api.app:app --reload
python test_api.py

# Test production
curl https://your-api.onrender.com/health
```

## 📖 Documentation

- **Quick Start**: [FILE_DISTRIBUTION.md](FILE_DISTRIBUTION.md)
- **Full Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Client Guide**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

**TL;DR:** Deploy `api/` to Render. Share docs + URL with clients.
