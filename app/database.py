import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "students.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_students_name ON students(name)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_students_course ON students(course)"
        )
        conn.commit()
