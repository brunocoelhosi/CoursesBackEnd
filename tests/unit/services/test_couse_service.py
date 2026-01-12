import pytest
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist

from courses.models import Course
from services.course_service import CourseService

@pytest.mark.django_db
class TestCourseService:

    def test_list_returns_only_published_courses(self):
        # Arrange
        Course.objects.create(title="Published", published=True)
        Course.objects.create(title="Unpublished", published=False)

        # Act
        result = CourseService.list()

        # Assert
        assert len(result) == 1
        assert result[0].title == "Published"

    def test_get_existing_course(self):
        course = Course.objects.create(title="Test Course", published=True)

        result = CourseService.get(course.id)

        assert result.id == course.id
        assert result.title == "Test Course"

    def test_get_nonexistent_course_raises_404(self):
        with pytest.raises(Exception):  # get_object_or_404 raises Http404
            CourseService.get(999)

    @patch("courses.tasks.generate_course_image_task.delay")
    def test_create_course_triggers_task(self, mock_delay):
        data = {"title": "New Course", "description": "Desc", "published": True}

        course = CourseService.create(data)

        assert course.title == data["title"]
        assert course.description == data["description"]
        assert course.image_url is None  # ✅ Imagem inicial nula
        mock_delay.assert_called_once_with(course.id)

    @patch("courses.tasks.generate_course_image_task.delay")
    def test_update_course_fields(self, mock_delay):
        course = Course.objects.create(title="Old Title", description="Old Desc", published=True)

        updated_data = {"title": "New Title", "description": None}  # 🔥 description None não atualiza
        updated_course = CourseService.update(course.id, updated_data)

        assert updated_course.title == "New Title"
        assert updated_course.description == "Old Desc"  # não foi sobrescrito
        mock_delay.assert_not_called()  # update não dispara task

    @patch("courses.tasks.generate_course_image_task.delay")
    def test_delete_course(self, mock_delay):
        course = Course.objects.create(title="To Delete", published=True)

        CourseService.delete(course.id)

        with pytest.raises(ObjectDoesNotExist):
            Course.objects.get(id=course.id)
        mock_delay.assert_not_called()  # delete não dispara task
