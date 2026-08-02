import logging
from typing import Dict, Any, List
from services.database_service import get_db_connection, init_db

logger = logging.getLogger(__name__)


def log_query_metrics(
    prompt: str,
    response_time_sec: float,
    feature_used: str = "General Gemini",
    model_name: str = "Gemini 2.5 Flash",
) -> bool:
    """
    Logs query execution metrics to SQLite query_logs table.

    Parameters
    ----------
    prompt : str
        User query prompt text.
    response_time_sec : float
        Elapsed execution latency in seconds.
    feature_used : str
        Nova feature pipeline name ('RAG', 'Vision AI', 'Browser Assistant', 'Desktop Automation', 'Productivity Engine', 'General Gemini').
    model_name : str
        LLM / Model identifier name.

    Returns
    -------
    bool
        True on success.
    """
    init_db()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO query_logs (prompt, response_time_sec, feature_used, model_name)
                VALUES (?, ?, ?, ?);
                """,
                (prompt[:250], float(response_time_sec), feature_used, model_name),
            )
            logger.info(f"Logged analytics query metrics: feature='{feature_used}', latency={response_time_sec}s")
            return True
    except Exception as e:
        logger.error(f"Failed to log query metrics: {e}")
        return False


def get_analytics_summary() -> Dict[str, Any]:
    """
    Aggregates metrics from query_logs table.

    Returns
    -------
    Dict[str, Any]
        Analytics metrics summary.
    """
    init_db()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 1. Total queries & avg latency
            cursor.execute("SELECT COUNT(*), AVG(response_time_sec) FROM query_logs;")
            row = cursor.fetchone()
            total_queries = row[0] if row and row[0] else 0
            avg_latency = round(row[1], 2) if row and row[1] else 0.0

            # 2. Feature distribution breakdown
            cursor.execute(
                """
                SELECT feature_used, COUNT(*) as count
                FROM query_logs
                GROUP BY feature_used
                ORDER BY count DESC;
                """
            )
            feature_rows = cursor.fetchall()
            feature_counts = {r["feature_used"]: r["count"] for r in feature_rows}

            # 3. Recent 10 queries
            cursor.execute(
                """
                SELECT prompt, response_time_sec, feature_used, model_name, created_at
                FROM query_logs
                ORDER BY id DESC
                LIMIT 10;
                """
            )
            recent_rows = cursor.fetchall()
            recent_queries = [dict(r) for r in recent_rows]

            return {
                "total_queries": total_queries,
                "avg_latency_sec": avg_latency,
                "feature_counts": feature_counts,
                "recent_queries": recent_queries,
            }

    except Exception as e:
        logger.error(f"Failed to fetch analytics summary: {e}")
        return {
            "total_queries": 0,
            "avg_latency_sec": 0.0,
            "feature_counts": {},
            "recent_queries": [],
        }


def generate_executive_report() -> str:
    """
    Generates a structured Markdown executive summary report of Nova usage & performance analytics.

    Returns
    -------
    str
        Markdown report string.
    """
    summary = get_analytics_summary()
    total = summary["total_queries"]
    avg_lat = summary["avg_latency_sec"]
    feature_counts = summary["feature_counts"]

    lines = [
        "# 📊 Nova Executive System Analytics & Performance Report",
        "",
        f"**Total Queries Processed**: `{total}`",
        f"**Average Latency**: `{avg_lat} seconds`",
        f"**System Efficiency Score**: `{max(90.0, 100.0 - (avg_lat * 2)):.1f}%`",
        "",
        "---",
        "## 🛠️ Feature Usage Breakdown",
        "",
    ]

    if feature_counts:
        for feat, count in feature_counts.items():
            pct = round((count / max(1, total)) * 100, 1)
            lines.append(f"- **{feat}**: `{count} queries` (`{pct}%`)")
    else:
        lines.append("*No query data recorded yet.*")

    lines.extend([
        "",
        "---",
        "## 🕒 Recent Activity Log",
        "",
    ])

    if summary["recent_queries"]:
        for q in summary["recent_queries"]:
            lines.append(f"- `[{q['created_at']}]` **{q['feature_used']}** ({q['response_time_sec']}s): *\"{q['prompt']}\"*")
    else:
        lines.append("*No activity logged.*")

    return "\n".join(lines)
