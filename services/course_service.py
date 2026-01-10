from courses.models import Course
from django.shortcuts import get_object_or_404

class CourseService:

    @staticmethod
    def list():
        return Course.objects.filter(published=True)

    @staticmethod
    def get(course_id: int):
        return get_object_or_404(Course, id=course_id)

    @staticmethod
    def create(data: dict):
        return Course.objects.create(**data)
    
    @staticmethod
    def update(course_id: int, data: dict):
        course = CourseService.get(course_id)

        for field, value in data.items():
            setattr(course, field, value)

        course.save()
        return course
    
    @staticmethod
    def delete(course_id: int):
        course = CourseService.get(course_id)
        course.delete()