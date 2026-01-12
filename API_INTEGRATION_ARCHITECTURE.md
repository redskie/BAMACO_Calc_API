# API Integration Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Your Website / Web Application              │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │ │
│  │  │   Rating    │  │Rating Range  │  │ Recommendation │ │ │
│  │  │ Calculator  │  │   Lookup     │  │    Engine      │ │ │
│  │  │ Component   │  │  Component   │  │   Component    │ │ │
│  │  └──────┬──────┘  └──────┬───────┘  └────────┬───────┘ │ │
│  │         │                 │                    │         │ │
│  │         └─────────────────┴────────────────────┘         │ │
│  │                           │                               │ │
│  │                    JavaScript API Client                 │ │
│  │                  (fetch, axios, etc.)                    │ │
│  └───────────────────────────┼───────────────────────────────┘ │
└────────────────────────────────┼─────────────────────────────────┘
                                 │
                          HTTPS Request
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    mai-tools API (Render)                       │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    FastAPI Application                    │ │
│  │                                                           │ │
│  │  GET  /health              → Health Check                │ │
│  │  GET  /ranks               → Rank Definitions            │ │
│  │  POST /rating              → Calculate Single Rating     │ │
│  │  POST /rating-range        → Get Rating Min/Max          │ │
│  │  POST /recommended-levels  → Get Level Recommendations   │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │           Core Rating Functions (Python)            │ │ │
│  │  │  • getRating()                                      │ │ │
│  │  │  • calculateRatingRange()                           │ │ │
│  │  │  • calculateRecommendedLevels()                     │ │ │
│  │  │  • getRankByAchievement()                           │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### Example 1: Calculate Rating

```
User Input:                API Request:               API Response:
┌─────────────┐           ┌──────────────┐           ┌─────────────┐
│ Level: 13.7 │           │ POST /rating │           │ rating:     │
│ Achv: 100.3%│  ──────>  │              │  ──────>  │   296.81    │
│             │           │ {            │           │ rank:       │
│ [Calculate] │           │  level: 13.7,│           │   "SSS"     │
└─────────────┘           │  achv: 100.3 │           └─────────────┘
                          │ }            │
                          └──────────────┘
```

### Example 2: Get Recommendations

```
User Input:                 API Request:                  API Response:
┌──────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ Target:      │          │ POST            │          │ SSS+: [...]     │
│  Rating 300  │ ──────>  │ /recommended-   │ ──────>  │ SSS:  [...]     │
│              │          │  levels         │          │ SS+:  [...]     │
│ [Get Charts] │          │                 │          │ ...             │
└──────────────┘          │ { rating: 300 } │          └─────────────────┘
                          └─────────────────┘
```

## Component Integration Pattern

### 1. Single Page Application (React/Vue/Angular)

```
┌─────────────────────────────────────────────────────┐
│                    App Container                    │
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   Header    │  │   Navbar    │  │   Sidebar  │ │
│  └─────────────┘  └─────────────┘  └────────────┘ │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │           Main Content Area                  │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │      Rating Calculator Card           │ │  │
│  │  │  • Input: Level                       │ │  │
│  │  │  • Input: Achievement                 │ │  │
│  │  │  • Button: Calculate ───> API Call    │ │  │
│  │  │  • Display: Result                    │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │      Recommendation Engine Card       │ │  │
│  │  │  • Input: Target Rating               │ │  │
│  │  │  • Button: Get Recs ───> API Call     │ │  │
│  │  │  • Display: Chart List by Rank        │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │      Rank Reference Table             │ │  │
│  │  │  • Auto-load ───> API Call            │ │  │
│  │  │  • Display: All Ranks Info            │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │              Footer                         │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 2. Multi-Page Website

```
Page Structure:

┌────────────────────────────────────┐
│         Home Page                  │
│  • Welcome Message                 │
│  • Quick Calculator                │
│    (Rating Calculator Component)   │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│      Calculator Page               │
│  • Full Rating Calculator          │
│  • Rating Range Lookup             │
│  • History/Saved Calculations      │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│    Recommendations Page            │
│  • Target Rating Input             │
│  • Chart Recommendations List      │
│  • Filtering Options               │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│      Reference Page                │
│  • Rank Table                      │
│  • Level Constants                 │
│  • FAQ                             │
└────────────────────────────────────┘
```

## API Client Architecture

### Recommended Structure

```javascript
// api-client.js
class MaiToolsAPIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.cache = new Map();
  }

  // Core methods
  async get(endpoint) { ... }
  async post(endpoint, data) { ... }

  // Business logic methods
  async calculateRating(level, achievement) { ... }
  async getRatingRange(level, rankTitle) { ... }
  async getRecommendations(targetRating) { ... }
  async getRanks() { ... } // with caching

  // Utility methods
  clearCache() { ... }
  setBaseURL(url) { ... }
}

// Usage in your app
const apiClient = new MaiToolsAPIClient('https://your-api.onrender.com');
export default apiClient;
```

## UI State Management Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     User Action                              │
│                  (Button Click, Form Submit)                 │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                 Validate Input                               │
│     (Check ranges, required fields, data types)              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              Set Loading State                               │
│        (Disable button, show spinner, clear errors)          │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   Make API Call                              │
│         (fetch/axios to mai-tools API endpoint)              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
                  ┌────┴────┐
                  │ Success? │
                  └─┬─────┬─┘
                    │     │
               Yes  │     │ No
                    │     │
                    ▼     ▼
      ┌──────────────┐   ┌──────────────┐
      │ Display      │   │ Display      │
      │ Results      │   │ Error        │
      │              │   │ Message      │
      └──────────────┘   └──────────────┘
                    │     │
                    │     │
                    ▼     ▼
      ┌──────────────────────────────────┐
      │      Clear Loading State          │
      │  (Re-enable button, hide spinner) │
      └───────────────────────────────────┘
```

## Error Handling Flow

```
API Call
   │
   ▼
┌──────────────────┐
│ Network Request  │
└─────────┬────────┘
          │
          ▼
     ┌────────┐
     │Response│
     └───┬────┘
         │
    ┌────┴─────┐
    │ Status?  │
    └─┬──────┬─┘
      │      │
  200 │      │ 4xx/5xx
      │      │
      ▼      ▼
   ┌────┐ ┌────────────────┐
   │ OK │ │ Parse Error    │
   └────┘ │ • 404: Invalid │
          │       rank     │
          │ • 422: Bad     │
          │       input    │
          │ • 500: Server  │
          │       error    │
          └────────┬───────┘
                   │
                   ▼
          ┌───────────────┐
          │ Show User-    │
          │ Friendly      │
          │ Error Message │
          └───────────────┘
                   │
                   ▼
          ┌───────────────┐
          │ Log Error     │
          │ (Console/     │
          │  Analytics)   │
          └───────────────┘
```

## Performance Optimization

### Caching Strategy

```
┌──────────────────────────────────────────────────────┐
│              Request for /ranks                      │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
                ┌──────────────┐
                │ Check Cache  │
                └──────┬───────┘
                       │
                  ┌────┴────┐
                  │ Cached? │
                  └─┬─────┬─┘
                    │     │
               Yes  │     │ No
                    │     │
                    ▼     ▼
      ┌──────────────┐   ┌──────────────┐
      │ Return       │   │ Make API     │
      │ Cached       │   │ Request      │
      │ Data         │   │              │
      └──────────────┘   └──────┬───────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ Store in Cache │
                        │ (1 hour TTL)   │
                        └────────┬───────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ Return Data    │
                        └────────────────┘
```

### Request Debouncing

```
User typing in input field:
   │
   "1"    "13"    "13."    "13.7"    [stops typing]
   │       │        │         │            │
   ▼       ▼        ▼         ▼            ▼
Reset   Reset    Reset     Reset      Wait 500ms
Timer   Timer    Timer     Timer          │
                                          ▼
                                   ┌──────────────┐
                                   │ Make API     │
                                   │ Request      │
                                   └──────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────────────────────────┐
│              Client-Side Validation                     │
│  • Check data types                                     │
│  • Validate ranges (level: 1-15, achievement: 0-101)    │
│  • Sanitize user input                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 HTTPS Only                              │
│  • All API calls over secure connection                │
│  • No sensitive data in query params                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Rate Limiting (Optional)                     │
│  • Implement client-side throttling                     │
│  • Respect server rate limits                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│             Error Message Handling                      │
│  • Don't expose sensitive error details                │
│  • Log errors securely                                  │
└─────────────────────────────────────────────────────────┘
```

## Deployment Checklist

### Before Going Live

- [ ] Replace `https://your-app-name.onrender.com` with actual Render URL
- [ ] Test all endpoints in production environment
- [ ] Set up error logging/monitoring (e.g., Sentry)
- [ ] Configure CORS if needed
- [ ] Set up analytics (optional)
- [ ] Test with actual user data
- [ ] Verify mobile responsiveness
- [ ] Check accessibility compliance
- [ ] Set up caching strategy
- [ ] Document API base URL for team

### Monitoring

```
┌─────────────────────────────────────────────────────────┐
│              Production Monitoring                      │
│                                                         │
│  • Health Check: GET /health every 5 minutes            │
│  • Response Time Tracking                               │
│  • Error Rate Monitoring                                │
│  • User Analytics (API usage patterns)                  │
└─────────────────────────────────────────────────────────┘
```

---

For detailed endpoint documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
