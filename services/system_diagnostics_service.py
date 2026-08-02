import os
import socket
import platform
import logging
import psutil
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def get_full_system_health() -> Dict[str, Any]:
    """
    Retrieves comprehensive real-time system metrics, hardware details, and top active processes.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing OS info, CPU, Memory, Disk, Network, and Top process list.
    """
    # 1. System & OS Info
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    sys_info = {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.architecture()[0],
        "python_version": platform.python_version(),
        "hostname": hostname,
        "local_ip": local_ip,
    }

    # 2. CPU Metrics
    cpu_pct = psutil.cpu_percent(interval=0.2)
    logical_cores = psutil.cpu_count(logical=True) or 1
    physical_cores = psutil.cpu_count(logical=False) or 1

    try:
        freq = psutil.cpu_freq()
        cpu_freq_mhz = round(freq.current, 1) if freq else 0.0
    except Exception:
        cpu_freq_mhz = 0.0

    cpu_metrics = {
        "percent": cpu_pct,
        "logical_cores": logical_cores,
        "physical_cores": physical_cores,
        "freq_mhz": cpu_freq_mhz,
    }

    # 3. Memory Metrics
    mem = psutil.virtual_memory()
    mem_metrics = {
        "percent": mem.percent,
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "free_gb": round(mem.free / (1024**3), 2),
    }

    # 4. Storage Disk Metrics
    try:
        disk = psutil.disk_usage("/")
        disk_metrics = {
            "percent": disk.percent,
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
        }
    except Exception:
        disk_metrics = {"percent": 0.0, "total_gb": 0.0, "used_gb": 0.0, "free_gb": 0.0}

    # 5. Top Active Processes Inspector (Sorted by Memory/CPU)
    top_processes: List[Dict[str, Any]] = []
    try:
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                pinfo = proc.info
                top_processes.append(
                    {
                        "pid": pinfo["pid"],
                        "name": pinfo["name"] or "Unknown",
                        "cpu_pct": round(pinfo["cpu_percent"] or 0.0, 1),
                        "mem_pct": round(pinfo["memory_percent"] or 0.0, 1),
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort processes by memory % descending
        top_processes.sort(key=lambda x: x["mem_pct"], reverse=True)
        top_processes = top_processes[:6]

    except Exception as e:
        logger.warning(f"Error inspecting top processes: {e}")

    return {
        "system_info": sys_info,
        "cpu": cpu_metrics,
        "memory": mem_metrics,
        "storage": disk_metrics,
        "top_processes": top_processes,
    }
