## ⚠️ Notice: Limited Maintenance

This project is no longer actively developed. Features may break at any time and may or may not receive fixes.

# Tools for maimai

## Use

Method 1. Follow https://myjian.github.io/mai-tools/#howto

Method 2. Install the userscript: https://github.com/myjian/mai-tools/blob/gh-pages/install-mai-tools.user.js . Your browser must support Tampermonkey or other userscript managers before you can install the userscript. Once the userscript is installed, mai-tools will be loaded automatically on every maimai-NET page.

## Build

    npm install
    npm run build

## Run

    npm start

## Develop

    npm run watch
    npm start

## Code Search

Using SourceGraph
https://sourcegraph.com/search?q=context%3Aglobal+repo%3A%5Egithub%5C.com%2Fmyjian%2Fmai-tools%24+GameRegion&patternType=standard&sm=1&groupBy=path (replace GameRegion with whatever you want to find)

## Python API (FastAPI)

This repo now ships a small FastAPI service that exposes the rating math used by the front-end.

```
┌─────────────────────────────────────────────────────────────────┐
│  What Goes Where?                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📤 Deploy to Render (Backend):                                │
│     • api/app.py                                                │
│     • requirements.txt                                          │
│     • render.yaml                                               │
│                                                                 │
│  📦 Share with Clients (Integration Package):                  │
│     • API_DOCUMENTATION.md                                      │
│     • API_QUICK_REFERENCE.md                                    │
│     • API_INTEGRATION_ARCHITECTURE.md                           │
│     • api_demo.html                                             │
│     • Your API URL (e.g., https://your-app.onrender.com)        │
│                                                                 │
│  💡 Quick Package: Run .\create-client-package.ps1              │
└─────────────────────────────────────────────────────────────────┘
```

### Run locally

1. Install Python 3.11+.
2. Install deps: `pip install -r requirements.txt`
3. Start the server: `uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload`
4. Open interactive docs at http://localhost:8000/docs

Available routes:

- `GET /health` – liveness check
- `GET /ranks` – rank definitions
- `POST /rating` – compute rating for `level` and `achievement`
- `POST /rating-range` – min/max rating for a given `level` and `rank_title`
- `POST /recommended-levels` – level/achievement combos to reach a target `rating`

### Deploy on Render

Render will pick up [render.yaml](render.yaml). Build installs `requirements.txt`; start command is `uvicorn api.app:app --host 0.0.0.0 --port 8000`. Set `PYTHON_VERSION` env var if you need a specific runtime.

### API Documentation

- **📖 Full Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete guide with examples, UI recommendations, and integration patterns
- **⚡ Quick Reference**: [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) - Fast lookup for endpoints and code snippets
- **🏗️ Integration Architecture**: [API_INTEGRATION_ARCHITECTURE.md](API_INTEGRATION_ARCHITECTURE.md) - System diagrams and integration patterns
- **🎮 Live Demo**: [api_demo.html](api_demo.html) - Interactive HTML demo (open in browser after starting the API server)
- **🚀 Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - What to deploy and what to share with clients
- **🧪 Test Results**: [TEST_REPORT.md](TEST_REPORT.md) - Test coverage and bug fixes

### File Distribution

**For Render Deployment** (upload to GitHub):

- `api/app.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration

**For Client Websites** (share with integrators):

- `API_DOCUMENTATION.md` - Integration guide
- `API_QUICK_REFERENCE.md` - Quick reference
- `API_INTEGRATION_ARCHITECTURE.md` - Architecture diagrams
- `api_demo.html` - Working demo
- Your production API URL

Run `.\create-client-package.ps1` to create a client distribution ZIP.
