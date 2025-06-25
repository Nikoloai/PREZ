# Presentation Generator API

This repository contains a simple FastAPI service for generating PDF presentations from JSON data.

## Setup
1. Install the required packages:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Run the service:
   ```bash
   python app.py
   ```
   The service will start on `0.0.0.0:8000` by default.
   Open `http://localhost:8000/` in your browser for a simple web interface.

## Endpoints
- `POST /create_presentation` – Accepts presentation data and returns a PDF file.
- `GET /health` – Basic health check that returns `{"status": "OK"}`.
- `GET /` – Simple HTML interface to submit presentation requests.

## Request Format
Example payload for `/create_presentation`:
```json
{
  "title": "AI Trends 2025",
  "slides": [
    {
      "slide_title": "Introduction",
      "slide_text": "In this presentation, we will cover the top AI trends for 2025.",
      "image_url": "https://example.com/ai-intro.png"
    }
  ]
}
```
