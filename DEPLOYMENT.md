# 🚀 Nova AI OS — Production Deployment Guide

This comprehensive guide covers all deployment strategies for **Nova AI Operating System**, ranging from local production servers to containerized Docker clusters and cloud platform deployments (AWS, DigitalOcean, Render, Vercel).

---

## 📋 Pre-Deployment Prerequisites

Before deploying Nova to production, ensure you have:

1. **Python 3.11+** installed.
2. **Node.js 18+** & **npm 10+** installed.
3. A valid **Google Gemini API Key** ([Get key from Google AI Studio](https://aistudio.google.com/)).
4. (Optional) **Ollama** installed locally for offline LLM synthesis (`llama3`, `mistral`).
5. (Optional) **Docker** and **Docker Compose** for containerized hosting.

---

## 💻 Strategy 1: Local Production Deployment (Single Port)

This strategy builds the React 18 + Vite frontend into optimized static assets (`frontend/dist`) and serves both the API endpoints and frontend interface through a single FastAPI Uvicorn process on port `8000`.

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/Sonal-sp/Nova-An-AI-voice-assistant-.git
cd Nova-An-AI-voice-assistant-

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies & React static build
cd frontend
npm install
npm run build
cd ..
```

### Step 3: Configure Environment File (`.env`)
Create `.env` at project root:
```env
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere
PORT=8000
HOST=0.0.0.0
LLM_TEMPERATURE=0.7
RAG_TOP_K=4
```

### Step 4: Run Unified Production Server
```bash
python -m uvicorn backend.server:app --host 0.0.0.0 --port 8000 --workers 4
```
Navigate to **`http://localhost:8000`** in Google Chrome or Microsoft Edge.

---

## 🐳 Strategy 2: Docker & Docker Compose Containerization

Containerization isolates dependencies, model weights, and system calls into a portable, reproducible image.

### Production `Dockerfile` Review
```dockerfile
FROM python:3.11-slim

# Install system dependencies & build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend compilation
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend, install node modules and build static SPA
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build
WORKDIR /app

# Copy backend source code
COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option A: Direct Docker Build & Run
```bash
# 1. Build Docker Image
docker build -t nova-ai-os:latest .

# 2. Run Docker Container
docker run -d \
  --name nova_os \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  nova-ai-os:latest
```

### Option B: Docker Compose
```yaml
version: '3.8'

services:
  nova:
    build: .
    container_name: nova_ai_os
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: always
```

Run Docker Compose:
```bash
docker-compose up -d --build
```

---

## ☁️ Strategy 3: Cloud Deployment (Render / AWS EC2 / DigitalOcean)

### Option A: Render / Railway Deployment (PaaS)
1. Push your repository to GitHub.
2. Create a **New Web Service** on Render or Railway.
3. Select **Docker** runtime environment.
4. Add Environment Variable:
   - `GEMINI_API_KEY`: `your_key_here`
5. Click **Deploy Web Service**. Render will automatically detect `Dockerfile`, build static React assets, and expose your live URL!

### Option B: AWS EC2 / DigitalOcean Ubuntu VM
1. Provision an Ubuntu 22.04 LTS instance (t3.medium or larger recommended).
2. SSH into your VM and install Docker:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose git
   ```
3. Clone repository and run Docker Compose:
   ```bash
   git clone https://github.com/Sonal-sp/Nova-An-AI-voice-assistant-.git
   cd Nova-An-AI-voice-assistant-
   echo "GEMINI_API_KEY=your_api_key" > .env
   sudo docker-compose up -d --build
   ```
4. Configure Nginx Reverse Proxy with SSL (Let's Encrypt / Certbot):
   ```nginx
   server {
       server_name nova.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

---

## 🔒 Security & Post-Deployment Checklist

- [x] **API Key Confidentiality**: Never commit `.env` or raw Gemini API keys to public repositories.
- [x] **HTTPS / SSL Encryption**: Ensure HTTPS is enabled on cloud deployments to permit Web Speech API audio recording permissions.
- [x] **CORS Configuration**: Restrict CORS origins in `backend/server.py` to specified domain names in multi-origin setups.
- [x] **Database Backup**: Periodically back up SQLite database files in `data/` (`nova_productivity.db`, `nova_integrations.db`).
- [x] **Master Suite Verification**: Run `python -m tests.test_master_production_suite` post-deployment.
