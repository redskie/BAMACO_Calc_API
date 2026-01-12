# Deployment and Distribution Guide

## 🚀 For Deploying to Render (Your API Backend)

### Required Files for GitHub/Render

Upload these files to your GitHub repository and Render will automatically deploy:

```
mai-tools/
├── api/
│   └── app.py                    ✅ REQUIRED - The FastAPI application
├── requirements.txt              ✅ REQUIRED - Python dependencies
├── render.yaml                   ✅ REQUIRED - Render configuration
└── README.md                     ⭐ RECOMMENDED - Project documentation
```

### Deployment Steps

1. **Push to GitHub:**

   ```bash
   git add api/ requirements.txt render.yaml
   git commit -m "Add Python API for rating calculations"
   git push origin gh-pages
   ```

2. **Deploy on Render:**

   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` and use these settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn api.app:app --host 0.0.0.0 --port 8000`
     - Environment: Python 3.11

3. **Get Your API URL:**
   - After deployment, Render provides a URL like:
     `https://mai-tools-api.onrender.com`
   - This is your production API base URL

### Optional Files (Don't Need to Deploy)

These files are useful but not required for the API to run:

- `test_api.py` - Local testing only
- `test_api_edge_cases.py` - Local testing only
- `api_demo.html` - Client-side demo (see below)
- All documentation `.md` files - For distribution to clients

---

## 📦 For Websites Using Your API (Client Distribution)

### Files to Share with Integration Partners

When a website wants to use your API, give them these files:

```
client-package/
├── API_DOCUMENTATION.md          ✅ ESSENTIAL - Complete integration guide
├── API_QUICK_REFERENCE.md        ✅ ESSENTIAL - Quick endpoint reference
├── API_INTEGRATION_ARCHITECTURE.md  ⭐ RECOMMENDED - System architecture
├── api_demo.html                 ⭐ RECOMMENDED - Working example they can run
└── API_BASE_URL.txt              ✅ ESSENTIAL - Your production URL
```

### Create Distribution Package

**Option 1: Create a ZIP file**

```bash
# Create a client package
mkdir client-package
cp API_DOCUMENTATION.md client-package/
cp API_QUICK_REFERENCE.md client-package/
cp API_INTEGRATION_ARCHITECTURE.md client-package/
cp api_demo.html client-package/

# Add your production URL
echo "https://mai-tools-api.onrender.com" > client-package/API_BASE_URL.txt

# Create ZIP
Compress-Archive -Path client-package/* -DestinationPath mai-tools-api-client.zip
```

**Option 2: Share via GitHub**

- Keep documentation in your GitHub repo
- Clients can view docs directly on GitHub
- Example: `https://github.com/myjian/mai-tools/blob/gh-pages/API_DOCUMENTATION.md`

**Option 3: Host documentation separately**

- Deploy docs to GitHub Pages
- Share the docs URL

---

## 📝 Quick Setup Instructions for Clients

Include this in your distribution:

### For Website Developers

**1. Read the Documentation**

- Start with `API_QUICK_REFERENCE.md` for a fast overview
- Study `API_DOCUMENTATION.md` for complete integration guide
- Review `api_demo.html` for a working example

**2. Update API URL**
Replace `API_BASE_URL` in your code with the production URL:

```javascript
// Change this in your code:
const API_BASE_URL = 'http://localhost:8000';

// To your production URL:
const API_BASE_URL = 'https://mai-tools-api.onrender.com';
```

**3. Test with the Demo**

1. Open `api_demo.html` in your browser
2. Update line 417 with your API URL
3. Test all three calculators work correctly

**4. Integrate into Your Website**

- Copy component code from `API_DOCUMENTATION.md`
- Follow integration patterns in `API_INTEGRATION_ARCHITECTURE.md`
- Implement error handling as documented

---

## 🗂️ Complete File Manifest

### Backend Files (Deploy to Render)

| File               | Purpose                     | Required?      |
| ------------------ | --------------------------- | -------------- |
| `api/app.py`       | FastAPI application core    | ✅ Yes         |
| `requirements.txt` | Python package dependencies | ✅ Yes         |
| `render.yaml`      | Render deployment config    | ✅ Yes         |
| `README.md`        | Project overview            | ⭐ Recommended |

### Client Files (Distribute to Website Developers)

| File                              | Purpose                          | Required?      |
| --------------------------------- | -------------------------------- | -------------- |
| `API_DOCUMENTATION.md`            | Complete API guide with examples | ✅ Yes         |
| `API_QUICK_REFERENCE.md`          | Quick endpoint lookup            | ✅ Yes         |
| `API_INTEGRATION_ARCHITECTURE.md` | System diagrams                  | ⭐ Recommended |
| `api_demo.html`                   | Working interactive demo         | ⭐ Recommended |
| Production API URL                | Your Render deployment URL       | ✅ Yes         |

### Internal/Development Files (Keep Local)

| File                     | Purpose          | Notes                  |
| ------------------------ | ---------------- | ---------------------- |
| `test_api.py`            | API tests        | For your testing only  |
| `test_api_edge_cases.py` | Edge case tests  | For your testing only  |
| `TEST_REPORT.md`         | Test results     | Internal documentation |
| `analysis.md`            | Project analysis | Internal documentation |

### Frontend Files (Original Project - Not Related to API)

These are the original TypeScript/React files for the mai-tools website:

- `src/` folder (TypeScript source)
- `public/` folder (HTML/data files)
- `webpack.config.js`
- `tsconfig.json`
- `package.json`
- `install-mai-tools.user.js`

**Note**: These files are separate from the new Python API. The API doesn't need them.

---

## ✅ Deployment Checklist

### Before Deploying to Render

- [ ] Test API locally: `uvicorn api.app:app --reload`
- [ ] Run test suite: `python test_api.py`
- [ ] Verify all endpoints return 200 status
- [ ] Check `requirements.txt` has correct versions
- [ ] Confirm `render.yaml` settings are correct
- [ ] Commit and push to GitHub

### After Deploying to Render

- [ ] Note your production URL (e.g., `https://mai-tools-api.onrender.com`)
- [ ] Test `/health` endpoint
- [ ] Test all 5 API endpoints with production URL
- [ ] Update `api_demo.html` with production URL
- [ ] Verify CORS settings if needed

### Before Distributing to Clients

- [ ] Create client package folder
- [ ] Include all documentation files
- [ ] Add a text file with your production API URL
- [ ] Test `api_demo.html` works with production URL
- [ ] Create ZIP archive or share GitHub link
- [ ] Write onboarding email with setup instructions

---

## 📧 Sample Client Onboarding Message

```
Subject: mai-tools API - Integration Package

Hello!

Thanks for your interest in integrating the mai-tools rating calculator API.

**Your API Base URL:**
https://mai-tools-api.onrender.com

**Getting Started:**
1. Download the attached client package (or visit GitHub)
2. Read API_QUICK_REFERENCE.md for a fast overview
3. Open api_demo.html in your browser to see it in action
4. Follow API_DOCUMENTATION.md for complete integration guide

**Key Endpoints:**
- POST /rating - Calculate rating from level & achievement
- POST /rating-range - Get min/max ratings for a rank
- POST /recommended-levels - Get chart recommendations

**Interactive Docs:**
Visit https://mai-tools-api.onrender.com/docs for Swagger UI

**Support:**
- Documentation: See attached files
- Issues: Open an issue on GitHub
- Questions: [Your contact method]

Happy coding!
```

---

## 🔧 Troubleshooting

### "My API URL isn't working"

- Check Render dashboard for deployment status
- Verify the URL is correct (no trailing slash)
- Test `/health` endpoint first

### "Client can't connect"

- Ensure HTTPS is used (not HTTP)
- Check for CORS issues (add CORS middleware if needed)
- Verify client is using correct endpoint paths

### "How do I update the API?"

1. Make changes to `api/app.py`
2. Commit and push to GitHub
3. Render auto-deploys on push
4. Notify clients of any breaking changes

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Render Docs**: https://render.com/docs
- **Original Project**: https://github.com/myjian/mai-tools

---

**Last Updated**: January 2026
**Maintained By**: myjian
