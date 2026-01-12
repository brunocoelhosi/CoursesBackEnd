from ninja import Schema
from datetime import datetime
from typing import Optional

class CourseIn(Schema):
    title: str
    description: str
    workload: int
    published: bool
    image_url: str | None
    video_url: str

class CourseOut(Schema):
    id: int
    title: str
    description: str
    created_at: datetime
    workload: int
    published: bool
    image_url: str | None
    video_url: str

class CourseUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    workload: Optional[int] = None
    published: Optional[bool] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class CourseVideoOut(Schema):
    id: int
    title: str
    video_url: str

class EnrollmentIn(Schema):
    course_id: int