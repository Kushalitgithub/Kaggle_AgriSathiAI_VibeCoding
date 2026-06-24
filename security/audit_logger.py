import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "agrisathi.db")

def log_event(user: str, role: str, action: str, details: str, status: str = "SUCCESS"):
    """
    Inserts a security audit log entry into the SQLite database.
    Status can be: SUCCESS, FAILED, BLOCKED, WARN
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO audit_logs (timestamp, user, role, action, details, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user, role, action, details, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error writing audit log: {e}")

def get_audit_logs(limit: int = 100):
    """
    Retrieves the most recent audit logs.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, user, role, action, details, status FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
        logs = cursor.fetchall()
        conn.close()
        return logs
    except Exception as e:
        print(f"Error fetching audit logs: {e}")
        return []
