from ninja import Router
from typing import List
from courses.schemas import CourseOut, CourseIn, CourseUpdate
from django.shortcuts import get_object_or_404
from courses.models import Course

from services.course_service import CourseService
from services.openai_service import generate_course_image

router = Router(tags=["Plataforma de Cursos Gratuitos - SME-SP"])

@router.get("/", response=List[CourseOut])
def list_courses(request):
    return CourseService.list()

@router.get("/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return CourseService.get(course_id)

@router.post("/", response=CourseOut)
def create_course(request, payload: CourseIn):
    image_url = generate_course_image(
        payload.title,
        payload.description
    )

    course = Course.objects.create(
        title=payload.title,
        description=payload.description,
        image_url=image_url
    )

    return course

@router.put("/{course_id}", response=CourseOut)
def update_course(request, course_id: int, payload: CourseUpdate):
    return CourseService.update(course_id, payload.dict())

@router.delete("/{course_id}")
def delete_course(request, course_id: int):
    CourseService.delete(course_id)
    return {"success": True}
