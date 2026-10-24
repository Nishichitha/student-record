import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import init_db
from app.crud import create_student, get_students, delete_student

init_db()

student = {
    'student_id': 'STU001',
    'name': 'Aisha Sharma',
    'dob': '2005-06-12',
    'email': 'aisha@example.com',
    'phone': '+91 9876543210',
    'course': 'B.Tech Computer Science',
    'address': 'Bengaluru',
    'enrollment_date': '2024-08-01'
}

create_student(student)
rows = get_students()
print(rows)

delete_student('STU001')
print('remaining', get_students())
