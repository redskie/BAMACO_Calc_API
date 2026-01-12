# mai-tools API Quick Reference

## Base URL

```
Production: https://bamaco-calc-api.onrender.com
Local: http://localhost:8000
```

## Endpoints

### Health Check

```bash
GET /health
```

### Get All Ranks

```bash
GET /ranks
```

### Calculate Rating

```bash
POST /rating
Content-Type: application/json

{
  "level": 13.7,
  "achievement": 100.3
}
```

### Get Rating Range

```bash
POST /rating-range
Content-Type: application/json

{
  "level": 13.7,
  "rank_title": "SSS"
}
```

### Get Recommended Levels

```bash
POST /recommended-levels
Content-Type: application/json

{
  "rating": 300
}
```

## Quick JavaScript Example

```javascript
const API_URL = 'https://your-app-name.onrender.com';

// Calculate rating
const response = await fetch(`${API_URL}/rating`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({level: 13.7, achievement: 100.3}),
});
const data = await response.json();
console.log(data); // { rating: 296.81, rank_title: "SSS", ... }
```

## Quick Python Example

```python
import requests

API_URL = 'https://your-app-name.onrender.com'

# Calculate rating
response = requests.post(
    f"{API_URL}/rating",
    json={"level": 13.7, "achievement": 100.3}
)
print(response.json())  # {'rating': 296.81, 'rank_title': 'SSS', ...}
```

## Quick cURL Example

```bash
# Calculate rating
curl -X POST https://your-app-name.onrender.com/rating \
  -H "Content-Type: application/json" \
  -d '{"level": 13.7, "achievement": 100.3}'

# Get ranks
curl https://your-app-name.onrender.com/ranks

# Get recommendations
curl -X POST https://your-app-name.onrender.com/recommended-levels \
  -H "Content-Type: application/json" \
  -d '{"rating": 300}'
```

## Valid Rank Names

SSS+, SSS, SS+, SS, S+, S, AAA, AA, A, BBB, BB, B, C, D

## Common Response Codes

- `200` - Success
- `404` - Rank not found
- `422` - Validation error
- `500` - Server error

---

📖 **Full Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
