## AI Usage
Used ChatGPT for guidance and test generation.

## Features Implemented
- Shorten long URL (POST /api/shorten)
- Redirect short code to original URL (GET /<short_code>)
- Track clicks and creation time (GET /api/stats/<short_code>)

## Assumptions
- In-memory store used (no DB)
- Short codes are randomly generated, 6-char alphanumeric

## Improvements If More Time
- Add persistence with SQLite/PostgreSQL
- Handle duplicate URLs more efficiently
- Add rate limiting or abuse protection
