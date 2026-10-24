from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    dob: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 7:
            raise ValueError("Phone number must contain at least 7 digits.")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 7:
            raise ValueError("Phone number must contain at least 7 digits.")
        return value


class StudentRecord(StudentBase):
    id: int


class StudentQuestion(BaseModel):
    question: str = Field(..., min_length=1)


class StudentResponse(StudentRecord):
    pass
