from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.database import get_connection


def normalize_student(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "student_id": row["student_id"],
        "name": row["name"],
        "dob": row["dob"],
        "email": row["email"],
        "phone": row["phone"],
        "course": row["course"],
        "address": row["address"],
        "enrollment_date": row["enrollment_date"],
    }


def get_students(name: Optional[str] = None, course: Optional[str] = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM students WHERE 1=1"
    params: List[Any] = []
    if name:
        query += " AND lower(name) LIKE lower(?)"
        params.append(f"%{name}%")
    if course:
        query += " AND lower(course) LIKE lower(?)"
        params.append(f"%{course}%")
    query += " ORDER BY id ASC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [normalize_student(dict(row)) for row in rows]


def get_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()
    if row is None:
        return None
    return normalize_student(dict(row))


def create_student(student_data: Dict[str, Any]) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO students (
                student_id, name, dob, email, phone, course, address, enrollment_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_data["student_id"],
                student_data["name"],
                str(student_data["dob"]),
                student_data.get("email"),
                student_data.get("phone"),
                student_data.get("course"),
                student_data.get("address"),
                str(student_data["enrollment_date"]) if student_data.get("enrollment_date") else None,
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM students WHERE id = ?", (new_id,)).fetchone()
    return normalize_student(dict(row))


def update_student(student_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    existing = get_student_by_id(student_id)
    if existing is None:
        return None

    allowed_fields = [
        "name",
        "dob",
        "email",
        "phone",
        "course",
        "address",
        "enrollment_date",
    ]
    filtered = {key: value for key, value in updates.items() if key in allowed_fields and value is not None}
    if not filtered:
        return existing

    assignments = ", ".join(f"{key} = ?" for key in filtered)
    values = [str(value) if key in {"dob", "enrollment_date"} else value for key, value in filtered.items()]
    with get_connection() as conn:
        conn.execute(
            f"UPDATE students SET {assignments} WHERE student_id = ?",
            (*values, student_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    return normalize_student(dict(row))


def delete_student(student_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
    return cursor.rowcount > 0
