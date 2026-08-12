import os
import sys
import json
import asyncio
import logging
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Ensure parent directory is in sys.path to import existing services seamlessly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import existing core Python services
import services.memory as memory_service
from services.chat_service import process_chat
from services.assistant import get_assistant_response
from services.gemini_service import ask_gemini, ask_gemini_vision
from services.document_service import create_document, get_document_statistics
from services.embedding_service import create_embeddings
from services.bm25_service import build_bm25_index
from services.desktop_service import launch_app, get_system_diagnostics
from services.system_diagnostics_service import get_full_system_health
from services.ollama_service import get_local_models, is_ollama_available
from services.productivity_service import (
    add_note, get_all_notes, delete_note,
    add_todo, get_all_todos, toggle_todo_status, delete_todo,
    get_daily_planner_summary
)
from services.integrations_service import (
    github_search_repos, slack_send_message, discord_send_message,
    gmail_search_unread, gdrive_search_files, gcalendar_list_events, notion_search_pages
)
from services.account_service import (
    get_all_user_integrations,
    connect_user_integration,
    disconnect_user_integration,
    test_integration_connection,
)
from utils.settings import load_settings, save_settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("nova-backend")

app = FastAPI(title="Nova AI Operating System API", version="2.5.0")

# Enable CORS for React Vite Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistent In-Memory Session Storage for Backend API mode
session_messages = []


# Pydantic Schemas
class ChatRequest(BaseModel):
    prompt: str
    selected_model: Optional[str] = "Gemini 2.5 Flash"
    document_context: Optional[str] = None
    web_context: Optional[str] = None


class LaunchAppRequest(BaseModel):
    app_name: str


class NoteRequest(BaseModel):
    title: str
    content: str
    tags: Optional[str] = ""


class TodoRequest(BaseModel):
    task: str
    due_date: Optional[str] = ""
    priority: Optional[str] = "Medium"


class SettingsRequest(BaseModel):
    settings: Dict[str, Any]


class WebhookMessageRequest(BaseModel):
    webhook_url: str
    text: str


class ConnectIntegrationRequest(BaseModel):
    service_name: str
    auth_token: Optional[str] = ""
    config: Optional[Dict[str, Any]] = None


@app.get("/api/health")
def get_health():
    """Returns live hardware performance & health diagnostics."""
    return get_full_system_health()


@app.get("/api/models")
def get_models():
    """Returns available LLM synthesis model options."""
    models = ["Gemini 2.5 Flash", "Gemini 2.0 Flash"]
    ollama_online = is_ollama_available()
    if ollama_online:
        for m in get_local_models():
            models.append(f"Ollama: {m}")
    else:
        models.extend(["Ollama: llama3:latest (Offline)", "Ollama: mistral:latest (Offline)"])
    return {"models": models, "ollama_available": ollama_online}


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Real-time Server-Sent Events (SSE) streaming LLM synthesis endpoint.
    Provides sub-100ms time-to-first-token generation.
    """
    global session_messages
    session_messages.append({"role": "user", "content": req.prompt})

    async def event_generator():
        try:
            # Run synchronous process_chat in thread pool to prevent blocking
            full_response = await asyncio.to_thread(
                process_chat, req.prompt, True, req.selected_model
            )

            if not full_response:
                text_content = "Command executed successfully."
                citations = []
                metadata = {}
            else:
                text_content = full_response.get("text", "")
                citations = full_response.get("citations", [])
                metadata = full_response.get("metadata", {})

            session_messages.append({"role": "assistant", "content": text_content})

            # Stream words chunk-by-chunk for real-time streaming feel
            words = text_content.split(" ") if text_content else ["Done."]
            for i, word in enumerate(words):
                chunk = word + (" " if i < len(words) - 1 else "")
                payload = json.dumps({"type": "token", "content": chunk})
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0.01)

            # Send final payload metadata & citations
            final_payload = json.dumps({
                "type": "done",
                "full_text": text_content,
                "citations": citations,
                "metadata": metadata,
            })
            yield f"data: {final_payload}\n\n"

        except Exception as e:
            logger.error(f"Stream generation error: {e}")
            err_payload = json.dumps({"type": "error", "content": f"⚠️ Error: {str(e)}"})
            yield f"data: {err_payload}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Indexes PDF document using Hybrid FAISS + BM25 search."""
    try:
        doc = create_document(file)
        faiss_idx, chunks = create_embeddings(doc["chunks"])
        bm25_idx = build_bm25_index(chunks)

        return {
            "status": "success",
            "filename": doc["filename"],
            "pages": doc["pages"],
            "chunk_count": doc["chunk_count"],
            "faiss_ready": faiss_idx is not None,
            "bm25_ready": bm25_idx is not None,
        }
    except Exception as e:
        logger.error(f"PDF upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vision")
async def vision_analysis(file: UploadFile = File(...), prompt: Optional[str] = Form("")):
    """Analyzes image mockup or document using Gemini Multimodal Vision."""
    try:
        from PIL import Image
        import io
        img_bytes = await file.read()
        pil_img = Image.open(io.BytesIO(img_bytes))
        result_text = ask_gemini_vision(pil_img, prompt)
        return {"status": "success", "analysis": result_text}
    except Exception as e:
        logger.error(f"Vision analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/launch-app")
def launch_desktop_app(req: LaunchAppRequest):
    """Launches local desktop software (VS Code, Chrome, Spotify, Calc)."""
    res = launch_app(req.app_name)
    return res


@app.get("/api/diagnostics")
def get_diagnostics():
    """Runs detailed system diagnostic benchmarks."""
    return get_system_diagnostics()


# Productivity Suite Routes
@app.get("/api/notes")
def get_notes(query: Optional[str] = ""):
    return {"notes": get_all_notes(query)}


@app.post("/api/notes")
def create_note_route(req: NoteRequest):
    add_note(req.title, req.content, req.tags)
    return {"status": "success"}


@app.delete("/api/notes/{note_id}")
def delete_note_route(note_id: int):
    delete_note(note_id)
    return {"status": "success"}


@app.get("/api/todos")
def get_todos(status_filter: Optional[str] = "all"):
    return {"todos": get_all_todos(status_filter)}


@app.post("/api/todos")
def create_todo_route(req: TodoRequest):
    add_todo(req.task, req.due_date, req.priority)
    return {"status": "success"}


@app.put("/api/todos/{todo_id}/toggle")
def toggle_todo_route(todo_id: int):
    toggle_todo_status(todo_id)
    return {"status": "success"}


@app.delete("/api/todos/{todo_id}")
def delete_todo_route(todo_id: int):
    delete_todo(todo_id)
    return {"status": "success"}


@app.get("/api/agenda")
def get_agenda():
    return get_daily_planner_summary()


# Cloud Integrations & User Accounts Routes
@app.get("/api/integrations")
def get_integrations():
    return {
        "user_integrations": get_all_user_integrations(),
        "github_repos": github_search_repos("nova-assistant"),
        "unread_gmail": gmail_search_unread(),
        "drive_files": gdrive_search_files("nova"),
        "calendar_events": gcalendar_list_events(),
        "notion_pages": notion_search_pages("nova"),
    }


@app.post("/api/user/integrations/connect")
def connect_user_integration_route(req: ConnectIntegrationRequest):
    return connect_user_integration(req.service_name, req.auth_token, req.config)


@app.post("/api/user/integrations/test")
def test_user_integration_route(req: ConnectIntegrationRequest):
    return test_integration_connection(req.service_name, req.auth_token, req.config)


@app.delete("/api/user/integrations/{service_name}")
def disconnect_user_integration_route(service_name: str):
    return disconnect_user_integration(service_name)


@app.post("/api/integrations/slack")
def post_slack(req: WebhookMessageRequest):
    return slack_send_message(req.webhook_url, req.text)


@app.post("/api/integrations/discord")
def post_discord(req: WebhookMessageRequest):
    return discord_send_message(req.webhook_url, req.text)


# Settings & History Routes
@app.get("/api/settings")
def get_settings_route():
    return load_settings()


@app.post("/api/settings")
def save_settings_route(req: SettingsRequest):
    save_settings(req.settings)
    return {"status": "success"}


@app.get("/api/messages")
def get_messages_route():
    return {"messages": session_messages}


@app.delete("/api/messages")
def clear_messages_route():
    global session_messages
    session_messages = []
    return {"status": "success"}


# Serve static built React Single Page App if frontend/dist exists
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="0.0.0.0", port=8000, reload=True)
