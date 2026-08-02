# 🚀 Nova Production Deployment & Setup Guide

This document outlines deployment configurations for running **Nova AI Assistant** locally, containerized with Docker, or deployed to cloud platforms.

---

## 1. Prerequisites
- **Python**: 3.10 or 3.11
- **API Keys**: Google Gemini API Key (`GEMINI_API_KEY`)
- **System Packages**: `ffmpeg`, `portaudio` (for audio STT/TTS)
- **Optional**: Ollama local server running at `http://localhost:11434` for offline model support

---

## 2. Local Environment Setup

```bash
# 1. Virtual Environment
python -m venv venv
venv\Scripts\activate

# 2. Dependencies
pip install -r requirements.txt

# 3. Launch Application
streamlit run app.py
```

---

## 3. Docker Container Deployment

```bash
# Build production Docker image
docker build -t nova-voice-assistant:latest .

# Run container exposing port 8501
docker run -d -p 8501:8501 --env GEMINI_API_KEY="your_api_key" --name nova nova-voice-assistant:latest
```

---

## 4. Docker Compose Orchestration

```yaml
version: '3.8'
services:
  nova-assistant:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d --build
```

---

## 5. Health Check Endpoint
Streamlit provides a built-in healthcheck route:
```http
GET http://localhost:8501/_stcore/health
```
Returns `200 OK` when the application is operational.
