# EWB Internship Project - Student Database CRUD API

This project is based on the EWB internship assignment for a Python backend development project. It implements a FastAPI application with SQLite persistence to manage student records with full CRUD support, plus an optional lightweight AI-style question feature using the stored records as context.

## Project objective

Build a Python backend app that allows users to create, read, update and delete student profiles. The application uses:

- FastAPI for the API layer
- SQLite for persistent storage
- Pydantic for request and response validation

## Features

- Create student records
- List all students or filter by name/course
- View an individual student profile
- Update a student record
- Delete a student record
- Optional database-grounded question answering
- Input validation and missing-record handling

## Project structure

```text
student-analysis/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── .gitignore
├── README.md
├── requirements.txt
├── students.db
└── run.py
```

## Prerequisites

- Python 3.10+
- pip
- virtual environment recommended

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
uvicorn app.main:app --reload
```

The API will run at:

- http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

## API endpoints

### Create a student

```http
POST /students
```

Example body:

```json
{
  "student_id": "STU001",
  "name": "Aisha Sharma",
  "dob": "2005-06-12",
  "email": "aisha@example.com",
  "phone": "+91 9876543210",
  "course": "B.Tech Computer Science",
  "address": "Bengaluru",
  "enrollment_date": "2024-08-01"
}
```

### List all students

```http
GET /students
```

### Get one student

```http
GET /students/{student_id}
```

### Update a student

```http
PUT /students/{student_id}
```

### Delete a student

```http
DELETE /students/{student_id}
```


## Sample request with curl

```bash
curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "Aisha Sharma",
    "dob": "2005-06-12",
    "email": "aisha@example.com",
    "phone": "+91 9876543210",
    "course": "B.Tech Computer Science",
    "address": "Bengaluru",
    "enrollment_date": "2024-08-01"
  }'
```
