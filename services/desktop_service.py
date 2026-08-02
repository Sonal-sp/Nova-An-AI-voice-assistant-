import os
import sys
import pathlib
import subprocess
import logging
import psutil
from typing import Dict, Any, List, Tuple, Optional

logger = logging.getLogger(__name__)


# ==========================================================
# 1. Desktop Application Launchers
# ==========================================================
def launch_app(app_name: str) -> Dict[str, Any]:
    """
    Launches a desktop application asynchronously using multi-strategy path, protocol URI, and shell fallback.

    Parameters
    ----------
    app_name : str
        Target application name or alias (e.g. 'vscode', 'chrome', 'spotify', 'notepad', 'calc').

    Returns
    -------
    Dict[str, Any]
        Dictionary with 'success', 'app_name', 'message'.
    """
    clean_name = app_name.strip().lower()

    # Special handling for Spotify on Windows
    if clean_name in ["spotify", "music"]:
        try:
            if sys.platform == "win32":
                # Strategy 1: Protocol URI (works for Microsoft Store & Win32 Spotify)
                os.startfile("spotify:")
                logger.info("Launched Spotify using protocol URI 'spotify:'")
                return {
                    "success": True,
                    "app_name": "Spotify",
                    "message": "🎵 Launched **Spotify** on your desktop.",
                }
        except Exception as e:
            logger.warning(f"Protocol URI launch for Spotify failed: {e}")

        # Strategy 2: Check Windows Store & AppData paths
        spotify_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\spotify.exe"),
            os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
        ]
        for sp_path in spotify_paths:
            if os.path.exists(sp_path):
                try:
                    subprocess.Popen([sp_path])
                    logger.info(f"Launched Spotify from path: {sp_path}")
                    return {
                        "success": True,
                        "app_name": "Spotify",
                        "message": "🎵 Launched **Spotify** on your desktop.",
                    }
                except Exception as ex:
                    logger.warning(f"Error launching Spotify from path {sp_path}: {ex}")

    # General app preset mappings & candidate commands
    presets = {
        "vscode": ["code", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
        "vs code": ["code", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
        "code": ["code", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
        "chrome": [
            "chrome",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "google chrome": [
            "chrome",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "spotify": ["spotify", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\spotify.exe")],
        "notepad": ["notepad"],
        "calc": ["calc"],
        "calculator": ["calc"],
        "paint": ["mspaint"],
        "mspaint": ["mspaint"],
        "terminal": ["cmd"],
        "cmd": ["cmd"],
        "powershell": ["powershell"],
        "explorer": ["explorer"],
    }

    candidates = presets.get(clean_name, [clean_name])

    for cmd_target in candidates:
        try:
            if os.path.isabs(cmd_target) and os.path.exists(cmd_target):
                subprocess.Popen([cmd_target])
                logger.info(f"Successfully launched desktop app via direct path: '{cmd_target}'")
                return {
                    "success": True,
                    "app_name": clean_name.capitalize(),
                    "message": f"💻 Launched **{clean_name.capitalize()}** on your desktop.",
                }
            elif sys.platform == "win32":
                subprocess.Popen(f"start {cmd_target}", shell=True)
                logger.info(f"Successfully launched desktop app via shell start: '{cmd_target}'")
                return {
                    "success": True,
                    "app_name": clean_name.capitalize(),
                    "message": f"💻 Launched **{clean_name.capitalize()}** on your desktop.",
                }
            else:
                subprocess.Popen([cmd_target])
                logger.info(f"Successfully launched desktop app: '{cmd_target}'")
                return {
                    "success": True,
                    "app_name": clean_name.capitalize(),
                    "message": f"💻 Launched **{clean_name.capitalize()}** on your desktop.",
                }
        except Exception as e:
            logger.warning(f"Attempt for candidate '{cmd_target}' failed: {e}")
            continue

    return {
        "success": False,
        "app_name": clean_name,
        "message": f"⚠️ Could not launch **{clean_name}**. Please ensure the application is installed.",
    }


# ==========================================================
# 2. File Search & Folder Management
# ==========================================================
def open_folder(folder_path: str) -> Dict[str, Any]:
    """
    Opens target directory path in Windows File Explorer.
    """
    clean_path = folder_path.strip().lower()
    user_home = pathlib.Path.home()

    shortcuts = {
        "downloads": str(user_home / "Downloads"),
        "documents": str(user_home / "Documents"),
        "desktop": str(user_home / "Desktop"),
        "workspace": os.getcwd(),
        "root": os.getcwd(),
    }

    target = shortcuts.get(clean_path, folder_path.strip())

    if not os.path.exists(target):
        rel_target = os.path.join(os.getcwd(), clean_path)
        if os.path.exists(rel_target):
            target = rel_target
        else:
            return {"success": False, "message": f"⚠️ Folder path not found: `{target}`"}

    try:
        if sys.platform == "win32":
            os.startfile(target)
        else:
            subprocess.Popen(["xdg-open", target])

        logger.info(f"Opened folder in File Explorer: {target}")
        return {
            "success": True,
            "path": target,
            "message": f"📂 Opened folder in File Explorer: `{target}`",
        }

    except Exception as e:
        logger.error(f"Error opening folder '{target}': {e}")
        return {"success": False, "message": f"⚠️ Error opening folder: {e}"}


def search_files(search_query: str, root_dir: Optional[str] = None, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Searches local file directory for matching filenames.
    """
    if not search_query or not search_query.strip():
        return []

    base_path = root_dir if (root_dir and os.path.exists(root_dir)) else os.getcwd()
    query_clean = search_query.strip().lower()
    matches: List[Dict[str, Any]] = []

    try:
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "__pycache__", "node_modules"]]

            for file in files:
                if query_clean in file.lower():
                    full_path = os.path.join(root, file)
                    try:
                        size_bytes = os.path.getsize(full_path)
                    except Exception:
                        size_bytes = 0

                    matches.append(
                        {
                            "name": file,
                            "path": full_path,
                            "size_kb": round(size_bytes / 1024, 1),
                        }
                    )
                    if len(matches) >= max_results:
                        break
            if len(matches) >= max_results:
                break

        logger.info(f"Found {len(matches)} files matching query '{search_query}'.")
        return matches

    except Exception as e:
        logger.error(f"Error searching files: {e}")
        return []


# ==========================================================
# 3. Clipboard Utilities
# ==========================================================
def get_clipboard_text() -> str:
    """
    Reads text content from system clipboard.
    """
    try:
        if sys.platform == "win32":
            cmd = ["powershell", "-command", "Get-Clipboard"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3.0)
            return res.stdout.strip()
    except Exception as e:
        logger.warning(f"Error reading clipboard: {e}")
    return ""


def set_clipboard_text(text: str) -> bool:
    """
    Sets text content into system clipboard.
    """
    if not text:
        return False

    try:
        if sys.platform == "win32":
            cmd = f'Set-Clipboard -Value "{text}"'
            subprocess.run(["powershell", "-command", cmd], capture_output=True, timeout=3.0)
            logger.info("Successfully copied text to system clipboard.")
            return True
    except Exception as e:
        logger.error(f"Error setting clipboard text: {e}")
    return False


# ==========================================================
# 4. System Diagnostics (psutil)
# ==========================================================
def get_system_diagnostics() -> Dict[str, Any]:
    """
    Retrieves real-time CPU, Memory, and System Process diagnostics using psutil.
    """
    try:
        cpu_pct = psutil.cpu_percent(interval=0.2)
        mem = psutil.virtual_memory()
        mem_pct = mem.percent
        mem_used_gb = round(mem.used / (1024**3), 2)
        mem_total_gb = round(mem.total / (1024**3), 2)
        process_count = len(psutil.pids())

        summary_md = f"""### 💻 System Diagnostics & Monitor
- **CPU Usage:** `{cpu_pct}%`
- **Memory Usage:** `{mem_pct}%` ({mem_used_gb} GB / {mem_total_gb} GB)
- **Active Processes:** `{process_count}`
"""

        return {
            "cpu_percent": cpu_pct,
            "memory_percent": mem_pct,
            "memory_used_gb": mem_used_gb,
            "memory_total_gb": mem_total_gb,
            "process_count": process_count,
            "summary_markdown": summary_md,
        }

    except Exception as e:
        logger.error(f"Error reading system diagnostics: {e}")
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "summary_markdown": f"⚠️ Could not read system stats: {e}",
        }
