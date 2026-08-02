import os
import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nova_productivity.db")


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Thread-safe context manager for SQLite database connections.
    Automatically commits transactions and closes connections.
    """
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database transaction error: {e}")
        raise e
    finally:
        conn.close()


def init_db() -> None:
    """
    Initializes SQLite tables for Notes, To-dos, Calendar Events, Reminders, and Query Analytics Logs.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 1. Notes Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # 2. To-dos Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    due_date TEXT DEFAULT '',
                    priority TEXT DEFAULT 'Medium',
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # 3. Calendar Events Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT DEFAULT '',
                    description TEXT DEFAULT '',
                    location TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # 4. Reminders Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reminder_text TEXT NOT NULL,
                    remind_at TEXT NOT NULL,
                    is_triggered INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # 5. Query Analytics Logs Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    response_time_sec REAL NOT NULL,
                    feature_used TEXT DEFAULT 'General Gemini',
                    model_name TEXT DEFAULT 'Gemini 2.5 Flash',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            logger.info("Successfully initialized Nova productivity & analytics SQLite database schema.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise e
