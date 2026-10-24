from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from app.crud import create_student, delete_student, get_student_by_id, get_students, update_student
from app.database import init_db
from app.models import StudentCreate, StudentQuestion, StudentRecord, StudentUpdate

app = FastAPI(
    title="Student Database CRUD API",
    description="FastAPI + SQLite backend for managing student records.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/students", response_model=List[StudentRecord])
def read_students(
    name: Optional[str] = Query(default=None),
    course: Optional[str] = Query(default=None),
) -> List[dict]:
    students = get_students(name=name, course=course)
    return students


@app.get("/students/{student_id}", response_model=StudentRecord)
def read_student(student_id: str) -> dict:
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students", response_model=StudentRecord, status_code=201)
def create_new_student(student: StudentCreate) -> dict:
    existing = get_student_by_id(student.student_id)
    if existing:
        raise HTTPException(status_code=400, detail="Student ID already exists")

    payload = student.model_dump()
    created = create_student(payload)
    return created


@app.put("/students/{student_id}", response_model=StudentRecord)
def update_existing_student(student_id: str, student: StudentUpdate) -> dict:
    payload = {key: value for key, value in student.model_dump().items() if value is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No update fields provided")

    updated = update_student(student_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@app.patch("/students/{student_id}", response_model=StudentRecord)
def patch_student(student_id: str, student: StudentUpdate) -> dict:
    payload = {key: value for key, value in student.model_dump().items() if value is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No update fields provided")

    updated = update_student(student_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@app.delete("/students/{student_id}")
def delete_student_record(student_id: str) -> dict:
    deleted = delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": f"Student {student_id} deleted successfully"}


@app.post("/students/ask")
def ask_about_students(question: StudentQuestion) -> dict:
    students = get_students()
    prompt = question.question.lower()

    if not students:
        return {"answer": "There are no student records in the database yet."}

    if "count" in prompt or "many" in prompt or "total" in prompt:
        return {"answer": f"There are {len(students)} students in the database."}

    if "after 2005" in prompt or "born after" in prompt:
        year = 2005
        filtered = [s for s in students if s["dob"] and s["dob"][:4].isdigit() and int(s["dob"][:4]) > year]
        if not filtered:
            return {"answer": "No students were born after 2005 in the current dataset."}
        names = ", ".join(student["name"] for student in filtered)
        return {"answer": f"Students born after 2005: {names}"}

    if "list" in prompt or "show" in prompt:
        names = ", ".join(student["name"] for student in students)
        return {"answer": f"Students in the database: {names}"}

    return {
        "answer": "I can answer questions such as student count or list students born after a certain year using the database records.",
        "records_used": len(students),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
