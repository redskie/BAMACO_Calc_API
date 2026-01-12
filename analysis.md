# Project Analysis

## What this repo does

- Front-end tools for SEGA maimai players: rating calculators, chart info, plate/achievement helpers, index page of bookmarklets and manuals (entry points listed in [webpack.config.js](webpack.config.js)).
- Implemented with React 18 + TypeScript, bundled by Webpack, and shipped as static assets copied from [public](public) into `build/`.
- Distributed either via the hosted site (`npm run start` serves the `build` folder) or via the userscript loader in [install-mai-tools.user.js](install-mai-tools.user.js).

## Structure at a glance

- Core scripts: [src/chart-info/main.ts](src/chart-info/main.ts), [src/classic-layout/main.tsx](src/classic-layout/main.tsx), [src/dx-achievement/main.tsx](src/dx-achievement/main.tsx), [src/index-page/main.tsx](src/index-page/main.tsx), [src/plate-progress/main.tsx](src/plate-progress/main.tsx), [src/rating-calculator/main.ts](src/rating-calculator/main.ts), [src/rating-visualizer/main.tsx](src/rating-visualizer/main.tsx).
- Shared domain logic lives in [src/common](src/common): rating/level helpers, rank definitions, song metadata helpers, fetching maimai-NET scores, and utility functions. Example: [src/common/rank-functions.ts](src/common/rank-functions.ts) holds rank constants (S–SSS+) and recommendation helpers; [src/common/rating-functions.ts](src/common/rating-functions.ts) computes ratings from level/achievement pairs.
- Public assets and data live under [public](public), copied verbatim by Webpack via CopyPlugin.
- Scripts under [src/scripts](src/scripts) are bundled to `build/scripts/*.js` for bookmarklet-like uses.

## Build and runtime

- Node 18+ required (see `engines` in [package.json](package.json)).
- Commands: `npm run build` for production bundle, `npm run watch` for dev build with watch, `npm start` to serve `build` on port 8080.
- Webpack emits `build/<entry>/main.bundle.js` per entry point; copies `public/` into `build/` unchanged. TypeScript is compiled in strict mode (except `strictNullChecks` off) per [tsconfig.json](tsconfig.json).

## Domain notes (for backend parity)

- Rating math: `getRating()` in [src/common/rating-functions.ts](src/common/rating-functions.ts) multiplies absolute level by achievement% and the rank factor (caps achievement at SSS+ 100.5%). `calculateRatingRange()` provides min/max for a given rank. Rank constants are defined in descending order in [src/common/rank-functions.ts](src/common/rank-functions.ts).
- Level presentation: helpers in [src/common/level-helper.ts](src/common/level-helper.ts) translate internal numeric levels to displayed levels (+ handling changes between game versions) and clamp maxima (MAX_LEVEL = 15).

## Gaps / risks observed

- No automated tests are present; changes to rating formulas or data need manual verification.
- Maintenance warning in [README.md](README.md) signals limited active development.
- Build is front-end only; there is no backend/API today, so hosting on Render as a Python API requires new scaffolding.

## Plan to expose a Python API (Render-friendly)

- Add a FastAPI-based service that mirrors key math utilities (rating computation, rating range, recommended levels) to offer programmatic access.
- Provide `requirements.txt` and `render.yaml` with `uvicorn api.app:app --host 0.0.0.0 --port 8000` start command for Render’s Python environment.
- Keep the existing front-end intact; the API will live in a new `api/` folder and can be deployed separately or alongside static assets if desired.
