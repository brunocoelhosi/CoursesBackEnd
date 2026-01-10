from ninja import Schema
from datetime import datetime

class CourseIn(Schema):
    title: str
    description: str
    workload: int
    published: bool

class CourseOut(Schema):
    id: int
    title: str
    description: str
    created_at: datetime
    workload: int
    published: bool
    image_url: str | None

class CourseUpdate(Schema):
    id: int
    title: str
    description: str
    workload: int
    published: bool
    image_url: str | None