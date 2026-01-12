# mai-tools API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Base URL](#base-url)
3. [API Endpoints](#api-endpoints)
4. [Integration Guide](#integration-guide)
5. [Frontend UI Recommendations](#frontend-ui-recommendations)
6. [Code Examples](#code-examples)
7. [Error Handling](#error-handling)

---

## Overview

The mai-tools API provides programmatic access to maimai (SEGA arcade rhythm game) rating calculations. This API enables developers to:

- Calculate player ratings based on chart levels and achievements
- Determine rating ranges for different rank tiers
- Get recommendations for which charts to play to reach target ratings
- Access rank definitions and thresholds

**Technology Stack**: FastAPI (Python 3.11+)
**Response Format**: JSON
**Authentication**: None required (public API)

---

## Base URL

**Local Development**: `http://localhost:8000`
**Production (Render)**: `https://your-app-name.onrender.com`

All endpoints return JSON responses with appropriate HTTP status codes.

---

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`
**Description**: Check if the API is running
**Authentication**: None

**Response**:

```json
{
  "status": "ok"
}
```

**Use Case**: System monitoring, uptime checks

---

### 2. Get All Ranks

**Endpoint**: `GET /ranks`
**Description**: Retrieve all rank definitions with their achievement thresholds and rating multipliers

**Response**:

```json
[
  {
    "title": "SSS+",
    "min_achv": 100.5,
    "factor": 0.224,
    "max_achv": null,
    "max_factor": null
  },
  {
    "title": "SSS",
    "min_achv": 100.0,
    "factor": 0.216,
    "max_achv": 100.4999,
    "max_factor": 0.222
  },
  ...
]
```

**Response Fields**:

- `title` (string): Rank name (SSS+, SSS, SS+, SS, S+, S, AAA, AA, A, BBB, BB, B, C, D)
- `min_achv` (float): Minimum achievement percentage required for this rank
- `factor` (float): Rating multiplier for this rank
- `max_achv` (float|null): Maximum achievement for special calculation
- `max_factor` (float|null): Special multiplier for max achievement

**Use Case**: Display rank information, populate rank selectors in UI

---

### 3. Calculate Rating

**Endpoint**: `POST /rating`
**Description**: Calculate the rating value for a specific chart level and achievement percentage

**Request Body**:

```json
{
  "level": 13.7,
  "achievement": 100.3
}
```

**Request Parameters**:

- `level` (float, required): Chart constant/level (typically 1.0 to 15.0)
  - Positive values: exact known levels
  - Negative values: estimated levels for utage charts
- `achievement` (float, required): Achievement percentage (0.0 to 101.0)
  - Capped at 100.5% (SSS+ threshold)

**Response**:

```json
{
  "rating": 296.80776,
  "rank_title": "SSS",
  "capped_achievement": 100.3
}
```

**Response Fields**:

- `rating` (float): Calculated rating value
- `rank_title` (string): Achieved rank based on achievement percentage
- `capped_achievement` (float): Achievement after capping at 100.5%

**Use Case**: Calculate individual chart ratings, display score results

**Example Scenarios**:

```json
// Perfect SSS+ play
{"level": 14.0, "achievement": 100.5} → {"rating": 314.496, "rank_title": "SSS+"}

// Strong SS play
{"level": 13.5, "achievement": 99.8} → {"rating": 288.441, "rank_title": "SS+"}

// S rank
{"level": 12.0, "achievement": 97.5} → {"rating": 234.0, "rank_title": "S"}
```

---

### 4. Calculate Rating Range

**Endpoint**: `POST /rating-range`
**Description**: Get the minimum and maximum possible rating for a given chart level at a specific rank

**Request Body**:

```json
{
  "level": 13.7,
  "rank_title": "SSS"
}
```

**Request Parameters**:

- `level` (float, required): Chart constant/level
- `rank_title` (string, required): Rank name (SSS+, SSS, SS+, SS, S+, S, AAA, AA, A, BBB, BB, B, C)

**Response**:

```json
{
  "min_rating": 295,
  "max_rating": 305,
  "rank_title": "SSS"
}
```

**Response Fields**:

- `min_rating` (int): Minimum rating achievable at this rank's lower threshold
- `max_rating` (int): Maximum rating achievable at this rank's upper threshold
- `rank_title` (string): Echo of the requested rank

**Use Case**: Show players the rating range they can expect for different rank targets

**Example Scenarios**:

```json
// Level 14.0, SSS+ rank
{"level": 14.0, "rank_title": "SSS+"} → {"min_rating": 314, "max_rating": 314}

// Level 13.0, S rank
{"level": 13.0, "rank_title": "S"} → {"min_rating": 252, "max_rating": 261}

// Level 12.5, AAA rank
{"level": 12.5, "rank_title": "AAA"} → {"min_rating": 262, "max_rating": 274}
```

---

### 5. Get Recommended Levels

**Endpoint**: `POST /recommended-levels`
**Description**: Calculate which chart levels and minimum achievements are needed to reach a target rating

**Request Body**:

```json
{
  "rating": 100
}
```

**Request Parameters**:

- `rating` (float, required): Target rating to achieve (typically 1 to 500+)

**Response**:

```json
{
  "SSS+": [
    {"lv": 4.5, "min_achv": 100.5, "rating": 101}
  ],
  "SSS": [
    {"lv": 4.6, "min_achv": 100.0, "rating": 100},
    {"lv": 4.7, "min_achv": 100.4721, "rating": 101}
  ],
  "SS+": [
    {"lv": 4.7, "min_achv": 99.5, "rating": 100},
    {"lv": 4.8, "min_achv": 99.9479, "rating": 101}
  ],
  ...
}
```

**Response Format**: Object with rank names as keys, each containing an array of level recommendations

**Level Recommendation Object**:

- `lv` (float): Chart level/constant
- `min_achv` (float): Minimum achievement percentage needed at this level
- `rating` (int): Actual rating this combination produces

**Use Case**: Help players identify which charts to play and what scores to aim for

**Example Scenarios**:

```json
// Low rating target (beginner)
{"rating": 50} → Suggests levels 2.5-3.5 across various ranks

// Medium rating target (intermediate)
{"rating": 200} → Suggests levels 9.5-11.5 across various ranks

// High rating target (advanced)
{"rating": 300} → Suggests levels 13.5-15.0 across SS+ to SSS+ ranks
```

---

## Integration Guide

### Step 1: API Connection Setup

```javascript
// JavaScript/TypeScript
const API_BASE_URL = 'https://your-app-name.onrender.com';

async function callAPI(endpoint, method = 'GET', data = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return await response.json();
}
```

```python
# Python
import requests

API_BASE_URL = 'https://your-app-name.onrender.com'

def call_api(endpoint, method='GET', data=None):
    url = f"{API_BASE_URL}{endpoint}"

    if method == 'GET':
        response = requests.get(url)
    else:
        response = requests.post(url, json=data)

    response.raise_for_status()
    return response.json()
```

### Step 2: Implement Core Functions

```javascript
// Calculate rating for a single play
async function calculateRating(level, achievement) {
  return await callAPI('/rating', 'POST', {level, achievement});
}

// Get rating range for a level/rank combination
async function getRatingRange(level, rankTitle) {
  return await callAPI('/rating-range', 'POST', {
    level,
    rank_title: rankTitle,
  });
}

// Get recommendations for target rating
async function getRecommendations(targetRating) {
  return await callAPI('/recommended-levels', 'POST', {
    rating: targetRating,
  });
}

// Get all ranks
async function getAllRanks() {
  return await callAPI('/ranks', 'GET');
}
```

### Step 3: Error Handling

```javascript
async function safeAPICall(apiFunction, ...args) {
  try {
    return await apiFunction(...args);
  } catch (error) {
    if (error.message.includes('404')) {
      console.error('Resource not found');
      return {error: 'Not found'};
    } else if (error.message.includes('422')) {
      console.error('Invalid input data');
      return {error: 'Validation failed'};
    } else if (error.message.includes('500')) {
      console.error('Server error');
      return {error: 'Server error'};
    } else {
      console.error('Network error:', error);
      return {error: 'Connection failed'};
    }
  }
}

// Usage
const result = await safeAPICall(calculateRating, 13.7, 100.3);
if (result.error) {
  // Handle error in UI
  showError(result.error);
} else {
  // Display result
  displayRating(result);
}
```

---

## Frontend UI Recommendations

### 1. Rating Calculator Component

**Purpose**: Allow users to input chart level and achievement to see their rating

**Required Elements**:

- **Input: Level** (number input, min: 1.0, max: 15.0, step: 0.1)

  - Label: "Chart Level" or "譜面レベル"
  - Placeholder: "13.7"
  - Validation: Must be between 1.0 and 15.0

- **Input: Achievement** (number input, min: 0.0, max: 101.0, step: 0.01)

  - Label: "Achievement %" or "達成率"
  - Placeholder: "100.30"
  - Validation: Must be between 0.0 and 101.0

- **Button: Calculate** (primary action button)

  - Text: "Calculate Rating" or "レートを計算"
  - Triggers: `POST /rating` with form data

- **Display: Result Panel**
  - Rating value (large, prominent display)
  - Rank badge/icon (color-coded by rank)
  - Capped achievement (if different from input)

**Sample HTML Structure**:

```html
<div class="rating-calculator">
  <h2>Rating Calculator</h2>

  <div class="input-group">
    <label for="level">Chart Level</label>
    <input type="number" id="level" min="1.0" max="15.0" step="0.1" placeholder="13.7" />
  </div>

  <div class="input-group">
    <label for="achievement">Achievement %</label>
    <input type="number" id="achievement" min="0" max="101" step="0.01" placeholder="100.30" />
  </div>

  <button id="calculate-btn" class="btn-primary">Calculate Rating</button>

  <div id="result" class="result-panel hidden">
    <div class="rating-display">
      <span class="rating-value">296.81</span>
      <span class="rank-badge rank-sss">SSS</span>
    </div>
    <div class="details">
      <p>Capped Achievement: 100.30%</p>
    </div>
  </div>
</div>
```

---

### 2. Rating Range Lookup Component

**Purpose**: Show players what ratings they can achieve at different ranks for a specific chart

**Required Elements**:

- **Input: Level** (number input, same as above)

- **Dropdown: Rank Selection** (select/dropdown)

  - Options: SSS+, SSS, SS+, SS, S+, S, AAA, AA, A, BBB, BB, B, C
  - Default: "S"

- **Button: Get Range** (secondary action button)

  - Text: "Get Rating Range"
  - Triggers: `POST /rating-range`

- **Display: Range Results**
  - Minimum rating (with label)
  - Maximum rating (with label)
  - Visual range indicator (progress bar or range slider)

**Sample HTML Structure**:

```html
<div class="rating-range-lookup">
  <h2>Rating Range by Rank</h2>

  <div class="input-group">
    <label for="range-level">Chart Level</label>
    <input type="number" id="range-level" min="1.0" max="15.0" step="0.1" placeholder="13.7" />
  </div>

  <div class="input-group">
    <label for="rank-select">Target Rank</label>
    <select id="rank-select">
      <option value="SSS+">SSS+</option>
      <option value="SSS">SSS</option>
      <option value="SS+">SS+</option>
      <option value="SS">SS</option>
      <option value="S+" selected>S+</option>
      <option value="S">S</option>
      <option value="AAA">AAA</option>
      <option value="AA">AA</option>
      <option value="A">A</option>
      <option value="BBB">BBB</option>
      <option value="BB">BB</option>
      <option value="B">B</option>
      <option value="C">C</option>
    </select>
  </div>

  <button id="get-range-btn" class="btn-secondary">Get Rating Range</button>

  <div id="range-result" class="range-panel hidden">
    <div class="range-display">
      <div class="range-value">
        <span class="min">Min: <strong>252</strong></span>
        <span class="max">Max: <strong>261</strong></span>
      </div>
      <div class="range-bar">
        <div class="range-fill" style="width: 100%"></div>
      </div>
    </div>
  </div>
</div>
```

---

### 3. Recommendation Engine Component

**Purpose**: Help players find charts to play to reach their target rating

**Required Elements**:

- **Input: Target Rating** (number input)

  - Label: "Target Rating" or "目標レート"
  - Placeholder: "300"
  - Validation: Positive number

- **Button: Get Recommendations** (primary action button)

  - Text: "Find Charts to Play"
  - Triggers: `POST /recommended-levels`

- **Display: Recommendations Table/List**
  - Grouped by rank (collapsible sections)
  - Each recommendation shows:
    - Chart level
    - Minimum achievement needed
    - Resulting rating
  - Sort options (by level, by difficulty)
  - Filter options (by rank tier)

**Sample HTML Structure**:

```html
<div class="recommendation-engine">
  <h2>Chart Recommendations</h2>

  <div class="input-group">
    <label for="target-rating">Target Rating</label>
    <input type="number" id="target-rating" min="1" placeholder="300" />
  </div>

  <button id="get-recommendations-btn" class="btn-primary">Find Charts to Play</button>

  <div id="recommendations" class="recommendations-panel hidden">
    <div class="rank-group">
      <h3 class="rank-header" data-rank="SSS+">
        <span class="rank-badge">SSS+</span>
        <span class="count">(1 option)</span>
        <span class="toggle">▼</span>
      </h3>
      <table class="recommendations-table">
        <thead>
          <tr>
            <th>Level</th>
            <th>Min Achievement</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>13.5</td>
            <td>100.50%</td>
            <td>304</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="rank-group">
      <h3 class="rank-header" data-rank="SSS">
        <span class="rank-badge">SSS</span>
        <span class="count">(3 options)</span>
        <span class="toggle">▼</span>
      </h3>
      <table class="recommendations-table">
        <thead>
          <tr>
            <th>Level</th>
            <th>Min Achievement</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>13.9</td>
            <td>100.00%</td>
            <td>300</td>
          </tr>
          <tr>
            <td>14.0</td>
            <td>100.35%</td>
            <td>302</td>
          </tr>
          <!-- more rows -->
        </tbody>
      </table>
    </div>

    <!-- More rank groups -->
  </div>
</div>
```

---

### 4. Rank Reference Component

**Purpose**: Display all rank tiers and their requirements

**Required Elements**:

- **Button: Load Ranks** (or auto-load on page load)

  - Triggers: `GET /ranks`

- **Display: Ranks Table**
  - Rank name with color coding
  - Minimum achievement threshold
  - Rating multiplier (factor)
  - Optional: achievement range

**Sample HTML Structure**:

```html
<div class="rank-reference">
  <h2>Rank Tiers</h2>

  <table class="ranks-table">
    <thead>
      <tr>
        <th>Rank</th>
        <th>Min Achievement</th>
        <th>Multiplier</th>
        <th>Achievement Range</th>
      </tr>
    </thead>
    <tbody id="ranks-tbody">
      <!-- Populated via API -->
      <tr class="rank-sss-plus">
        <td><span class="rank-badge">SSS+</span></td>
        <td>100.50%</td>
        <td>0.224</td>
        <td>100.50% - 101.00%</td>
      </tr>
      <tr class="rank-sss">
        <td><span class="rank-badge">SSS</span></td>
        <td>100.00%</td>
        <td>0.216</td>
        <td>100.00% - 100.49%</td>
      </tr>
      <!-- More rows -->
    </tbody>
  </table>
</div>
```

---

### 5. Bulk Rating Calculator (Advanced)

**Purpose**: Calculate ratings for multiple charts at once

**Required Elements**:

- **Textarea/CSV Input**: Paste multiple chart data

  - Format: "level,achievement" per line
  - Example:
    ```
    13.7,100.3
    14.0,99.8
    12.5,100.5
    ```

- **Button: Calculate All**

  - Loops through each line, calls `/rating` endpoint
  - Shows progress indicator

- **Display: Results Table**
  - Chart number
  - Level
  - Achievement
  - Rating
  - Rank
  - Export button (CSV/JSON)

---

## Code Examples

### Complete React Component Example

```jsx
import React, {useState} from 'react';

const RatingCalculator = () => {
  const [level, setLevel] = useState('');
  const [achievement, setAchievement] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'https://your-app-name.onrender.com';

  const calculateRating = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/rating`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          level: parseFloat(level),
          achievement: parseFloat(achievement),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate rating');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rating-calculator">
      <h2>Rating Calculator</h2>

      <div className="form-group">
        <label htmlFor="level">Chart Level</label>
        <input
          type="number"
          id="level"
          value={level}
          onChange={(e) => setLevel(e.target.value)}
          min="1.0"
          max="15.0"
          step="0.1"
          placeholder="13.7"
        />
      </div>

      <div className="form-group">
        <label htmlFor="achievement">Achievement %</label>
        <input
          type="number"
          id="achievement"
          value={achievement}
          onChange={(e) => setAchievement(e.target.value)}
          min="0"
          max="101"
          step="0.01"
          placeholder="100.30"
        />
      </div>

      <button
        onClick={calculateRating}
        disabled={loading || !level || !achievement}
        className="btn-primary"
      >
        {loading ? 'Calculating...' : 'Calculate Rating'}
      </button>

      {error && <div className="error-message">Error: {error}</div>}

      {result && (
        <div className="result-panel">
          <div className="rating-display">
            <div className="rating-value">{result.rating.toFixed(2)}</div>
            <div className={`rank-badge rank-${result.rank_title.toLowerCase()}`}>
              {result.rank_title}
            </div>
          </div>
          <div className="details">
            <p>Capped Achievement: {result.capped_achievement.toFixed(2)}%</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default RatingCalculator;
```

### Complete Vue.js Component Example

```vue
<template>
  <div class="recommendation-engine">
    <h2>Chart Recommendations</h2>

    <div class="input-group">
      <label for="target-rating">Target Rating</label>
      <input
        v-model.number="targetRating"
        type="number"
        id="target-rating"
        placeholder="300"
        min="1"
      />
    </div>

    <button @click="getRecommendations" :disabled="loading" class="btn-primary">
      {{ loading ? 'Loading...' : 'Get Recommendations' }}
    </button>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="recommendations" class="recommendations-panel">
      <div v-for="(levels, rank) in recommendations" :key="rank" class="rank-group">
        <h3 class="rank-header" @click="toggleRank(rank)">
          <span class="rank-badge">{{ rank }}</span>
          <span class="count">({{ levels.length }} options)</span>
          <span class="toggle">{{ expandedRanks[rank] ? '▼' : '►' }}</span>
        </h3>

        <table v-if="expandedRanks[rank]" class="recommendations-table">
          <thead>
            <tr>
              <th>Level</th>
              <th>Min Achievement</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(level, index) in levels" :key="index">
              <td>{{ level.lv.toFixed(1) }}</td>
              <td>{{ level.min_achv.toFixed(2) }}%</td>
              <td>{{ level.rating }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendationEngine',
  data() {
    return {
      targetRating: '',
      recommendations: null,
      loading: false,
      error: null,
      expandedRanks: {},
      apiBaseUrl: 'https://your-app-name.onrender.com',
    };
  },
  methods: {
    async getRecommendations() {
      if (!this.targetRating) {
        this.error = 'Please enter a target rating';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(`${this.apiBaseUrl}/recommended-levels`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rating: this.targetRating,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to get recommendations');
        }

        this.recommendations = await response.json();

        // Expand first rank by default
        const firstRank = Object.keys(this.recommendations)[0];
        if (firstRank) {
          this.expandedRanks = {[firstRank]: true};
        }
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    toggleRank(rank) {
      this.expandedRanks = {
        ...this.expandedRanks,
        [rank]: !this.expandedRanks[rank],
      };
    },
  },
};
</script>
```

### Vanilla JavaScript Example

```javascript
// rating-calculator.js
class RatingCalculatorUI {
  constructor(containerId, apiBaseUrl) {
    this.container = document.getElementById(containerId);
    this.apiBaseUrl = apiBaseUrl;
    this.init();
  }

  init() {
    this.render();
    this.attachEventListeners();
  }

  render() {
    this.container.innerHTML = `
      <div class="rating-calculator">
        <h2>Rating Calculator</h2>

        <div class="input-group">
          <label for="level">Chart Level</label>
          <input type="number" id="level" min="1.0" max="15.0" step="0.1" placeholder="13.7" />
        </div>

        <div class="input-group">
          <label for="achievement">Achievement %</label>
          <input type="number" id="achievement" min="0" max="101" step="0.01" placeholder="100.30" />
        </div>

        <button id="calculate-btn" class="btn-primary">Calculate Rating</button>

        <div id="result" class="result-panel hidden"></div>
        <div id="error" class="error-message hidden"></div>
      </div>
    `;
  }

  attachEventListeners() {
    const calculateBtn = this.container.querySelector('#calculate-btn');
    calculateBtn.addEventListener('click', () => this.calculateRating());
  }

  async calculateRating() {
    const level = parseFloat(this.container.querySelector('#level').value);
    const achievement = parseFloat(this.container.querySelector('#achievement').value);
    const resultDiv = this.container.querySelector('#result');
    const errorDiv = this.container.querySelector('#error');

    // Validation
    if (isNaN(level) || isNaN(achievement)) {
      this.showError('Please enter valid numbers');
      return;
    }

    if (level < 1.0 || level > 15.0) {
      this.showError('Level must be between 1.0 and 15.0');
      return;
    }

    if (achievement < 0 || achievement > 101) {
      this.showError('Achievement must be between 0 and 101');
      return;
    }

    // Clear previous results
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');

    try {
      const response = await fetch(`${this.apiBaseUrl}/rating`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({level, achievement}),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      this.displayResult(data);
    } catch (error) {
      this.showError(`Failed to calculate rating: ${error.message}`);
    }
  }

  displayResult(data) {
    const resultDiv = this.container.querySelector('#result');
    const rankClass = data.rank_title.toLowerCase().replace('+', '-plus');

    resultDiv.innerHTML = `
      <div class="rating-display">
        <div class="rating-value">${data.rating.toFixed(2)}</div>
        <div class="rank-badge rank-${rankClass}">${data.rank_title}</div>
      </div>
      <div class="details">
        <p>Capped Achievement: ${data.capped_achievement.toFixed(2)}%</p>
      </div>
    `;
    resultDiv.classList.remove('hidden');
  }

  showError(message) {
    const errorDiv = this.container.querySelector('#error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
  }
}

// Usage
const calculator = new RatingCalculatorUI(
  'calculator-container',
  'https://your-app-name.onrender.com'
);
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning          | Cause                                 | Solution                    |
| ---- | ---------------- | ------------------------------------- | --------------------------- |
| 200  | Success          | Request processed successfully        | Display results             |
| 404  | Not Found        | Invalid rank title in `/rating-range` | Verify rank name is correct |
| 422  | Validation Error | Missing or invalid request parameters | Check request body format   |
| 500  | Server Error     | Internal server error                 | Retry or contact support    |

### Common Errors and Solutions

**Error: "Rank not found"**

- **Cause**: Invalid rank title in `/rating-range` request
- **Solution**: Use only valid rank names: SSS+, SSS, SS+, SS, S+, S, AAA, AA, A, BBB, BB, B, C

**Error: Validation failed (422)**

- **Cause**: Missing required fields or wrong data types
- **Solution**: Ensure all required fields are included and have correct types (numbers for level/achievement)

**Error: Connection timeout**

- **Cause**: Network issues or server not responding
- **Solution**: Implement retry logic with exponential backoff

**Example Error Handler**:

```javascript
function handleAPIError(error, response) {
  if (!response) {
    return 'Network error. Please check your connection.';
  }

  switch (response.status) {
    case 404:
      return 'Invalid rank name. Please select from the available options.';
    case 422:
      return 'Invalid input. Please check your level and achievement values.';
    case 500:
      return 'Server error. Please try again later.';
    default:
      return `Unexpected error: ${error.message}`;
  }
}
```

---

## Best Practices

### 1. Caching

Cache rank definitions since they rarely change:

```javascript
let ranksCache = null;
let cacheTimestamp = null;
const CACHE_DURATION = 3600000; // 1 hour

async function getRanks() {
  const now = Date.now();

  if (ranksCache && cacheTimestamp && now - cacheTimestamp < CACHE_DURATION) {
    return ranksCache;
  }

  ranksCache = await fetch(`${API_BASE_URL}/ranks`).then((r) => r.json());
  cacheTimestamp = now;

  return ranksCache;
}
```

### 2. Input Debouncing

Debounce user input to avoid excessive API calls:

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const debouncedCalculate = debounce(calculateRating, 500);
```

### 3. Loading States

Always show loading indicators during API calls:

```javascript
function setLoading(isLoading) {
  const button = document.querySelector('#calculate-btn');
  const spinner = document.querySelector('.spinner');

  if (isLoading) {
    button.disabled = true;
    button.textContent = 'Calculating...';
    spinner.classList.remove('hidden');
  } else {
    button.disabled = false;
    button.textContent = 'Calculate Rating';
    spinner.classList.add('hidden');
  }
}
```

### 4. Progressive Enhancement

Ensure basic functionality works without JavaScript, then enhance:

```html
<form action="https://your-app-name.onrender.com/rating" method="GET">
  <input name="level" type="number" required />
  <input name="achievement" type="number" required />
  <button type="submit">Calculate</button>
</form>

<script>
  // Enhance with JavaScript for better UX
  enhanceWithAjax();
</script>
```

### 5. Accessibility

- Use semantic HTML
- Add ARIA labels for screen readers
- Ensure keyboard navigation works
- Provide alternative text for visual elements

```html
<button
  aria-label="Calculate rating for entered chart level and achievement"
  aria-describedby="calc-help"
>
  Calculate
</button>
<span id="calc-help" class="sr-only">
  Calculates your rating based on chart difficulty and your score
</span>
```

---

## Additional Resources

- **API Interactive Docs**: `https://your-app-name.onrender.com/docs`
- **OpenAPI Spec**: `https://your-app-name.onrender.com/openapi.json`
- **Source Code**: [GitHub Repository](https://github.com/myjian/mai-tools)

---

## Support

For bugs or feature requests, please open an issue on GitHub or contact the maintainers.

**Last Updated**: January 2026
**API Version**: 0.1.0
