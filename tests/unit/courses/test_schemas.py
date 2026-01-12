import pytest
from datetime import datetime
from ninja.errors import ValidationError

from courses.schemas import CourseIn, CourseOut, CourseUpdate, CourseVideoOut, EnrollmentIn

class TestCourseSchemas:

    def test_course_in_valid_data(self):
        data = {
            "title": "Curso Teste",
            "description": "Descrição do curso",
            "workload": 10,
            "published": True,
            "image_url": None,
            "video_url": "http://video.com/video.mp4"
        }
        course = CourseIn(**data)
        assert course.title == data["title"]
        assert course.image_url is None

    def test_course_out_valid_data(self):
        data = {
            "id": 1,
            "title": "Curso Teste",
            "description": "Descrição do curso",
            "created_at": datetime.now(),
            "workload": 10,
            "published": True,
            "image_url": None,
            "video_url": "http://video.com/video.mp4"
        }
        course = CourseOut(**data)
        assert course.id == data["id"]
        assert course.created_at == data["created_at"]

    def test_course_update_optional_fields(self):
        # Pode criar com nenhum campo
        update = CourseUpdate()
        assert update.title is None
        assert update.published is None

        # Pode criar com alguns campos
        update = CourseUpdate(title="Novo título", workload=20)
        assert update.title == "Novo título"
        assert update.workload == 20

    def test_course_video_out_valid_data(self):
        data = {"id": 1, "title": "Curso Teste", "video_url": "http://video.com/video.mp4"}
        video = CourseVideoOut(**data)
        assert video.id == data["id"]
        assert video.video_url == data["video_url"]

    def test_enrollment_in_valid_data(self):
        enrollment = EnrollmentIn(course_id=123)
        assert enrollment.course_id == 123

    def test_course_in_invalid_data(self):
        # workload deve ser int
        data = {
            "title": "Curso Teste",
            "description": "Descrição",
            "workload": "dez",  # inválido
            "published": True,
            "image_url": None,
            "video_url": "http://video.com/video.mp4"
        }
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            CourseIn(**data)

