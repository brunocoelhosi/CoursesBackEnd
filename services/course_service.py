from courses.models import Course
from django.shortcuts import get_object_or_404
from services.openai_service import generate_course_image
from courses.schemas import CourseIn
from courses.tasks import generate_course_image_task

class CourseService:

    @staticmethod
    def list():
        return Course.objects.filter(published=True)

    @staticmethod
    def get(course_id: int):
        return get_object_or_404(Course, id=course_id)

    """    
    @staticmethod
    def create(data: dict):
        if "image_url" not in data or not data["image_url"]:
            data["image_url"] = generate_course_image(
                title=data.get("title", ""),
                description=data.get("description", ""),
            )

        return Course.objects.create(**data)"""
    @staticmethod
    def create(data: dict):
        # 1️⃣ NÃO gera imagem aqui
        data["image_url"] = None

        # 2️⃣ Cria o curso imediatamente
        course = Course.objects.create(**data)

        # 3️⃣ Dispara geração assíncrona
        generate_course_image_task.delay(course.id)

        return course

    @staticmethod
    def update(course_id: int, data: dict):
        course = CourseService.get(course_id)

        for field, value in data.items():
            if value is not None:   # 🔥 ESSENCIAL
                setattr(course, field, value)

        course.save()
        return course
    
    @staticmethod
    def delete(course_id: int):
        course = CourseService.get(course_id)
        course.delete()