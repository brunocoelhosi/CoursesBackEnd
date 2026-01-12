import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from django.contrib.auth.models import AnonymousUser
from courses.models import Course, Enrollment
from courses.schemas import CourseIn, CourseUpdate, EnrollmentIn
from services.course_service import CourseService
from courses.api import (
    list_courses, get_course, create_course, update_course,
    delete_course, get_course_video, my_courses, enroll_course
)

@pytest.mark.django_db
class TestCourseRouter:

    def test_list_courses_calls_service(self):
        with patch.object(CourseService, "list", return_value=["course1", "course2"]) as mock_list:
            result = list_courses(MagicMock())
            assert result == ["course1", "course2"]
            mock_list.assert_called_once()

    def test_get_course_calls_service(self):
        course = Course(id=1, title="Teste", description="Desc", workload=10, published=True, image_url=None, video_url="url")
        with patch.object(CourseService, "get", return_value=course) as mock_get:
            result = get_course(MagicMock(), course_id=1)
            assert result == course
            mock_get.assert_called_once_with(1)

    def test_create_course_non_staff_returns_403(self):
        request = MagicMock()
        request.user.is_staff = False
        payload = CourseIn(title="t", description="d", workload=1, published=True, image_url=None, video_url="url")
        status, data = create_course(request, payload)
        assert status == 403
        assert "Apenas admins" in data["detail"]

    def test_create_course_calls_service_for_admin(self):
        request = MagicMock()
        request.user.is_staff = True
        payload = CourseIn(title="t", description="d", workload=1, published=True, image_url=None, video_url="url")
        course = MagicMock()
        with patch.object(CourseService, "create", return_value=course) as mock_create:
            result = create_course(request, payload)
            assert result == course
            mock_create.assert_called_once_with(payload.dict())

    def test_update_course_non_staff_returns_403(self):
        request = MagicMock()
        request.user.is_staff = False
        payload = CourseUpdate(title="novo")
        status, data = update_course(request, 1, payload)
        assert status == 403
        assert "Apenas admins" in data["detail"]

    def test_update_course_calls_service_for_admin(self):
        request = MagicMock()
        request.user.is_staff = True
        payload = CourseUpdate(title="novo")
        course = MagicMock()
        with patch.object(CourseService, "update", return_value=course) as mock_update:
            result = update_course(request, 1, payload)
            assert result == course
            mock_update.assert_called_once_with(1, payload.dict(exclude_unset=True))

    def test_delete_course_calls_service(self):
        request = MagicMock()
        with patch.object(CourseService, "delete") as mock_delete:
            result = delete_course(request, 1)
            assert result == {"success": True}
            mock_delete.assert_called_once_with(1)

    def test_get_course_video_not_enrolled_returns_403(self):
        request = MagicMock()
        request.user = MagicMock()
        course = Course(id=1, title="Curso", description="d", workload=1, published=True, image_url=None, video_url="url")
        with patch("courses.api.get_object_or_404", return_value=course):
            with patch("courses.api.Enrollment.objects.filter") as mock_filter:
                mock_filter.return_value.exists.return_value = False
                status, data = get_course_video(request, 1)
                assert status == 403
                assert "não está inscrito" in data["detail"]

    def test_get_course_video_enrolled_returns_data(self):
        request = MagicMock()
        request.user = MagicMock()
        course = Course(id=1, title="Curso", description="d", workload=1, published=True, image_url=None, video_url="url")
        with patch("courses.api.get_object_or_404", return_value=course):
            with patch("courses.api.Enrollment.objects.filter") as mock_filter:
                mock_filter.return_value.exists.return_value = True
                result = get_course_video(request, 1)
                assert result["id"] == 1
                assert result["title"] == "Curso"

    def test_enroll_course_already_enrolled_returns_detail(self):
        request = MagicMock()
        request.user = MagicMock()
        payload = EnrollmentIn(course_id=1)
        course = MagicMock()
        with patch("courses.api.get_object_or_404", return_value=course):
            with patch("courses.api.Enrollment.objects.get_or_create", return_value=(course, False)):
                status, data = enroll_course(request, payload)
                assert status == 200
                assert "já matriculado" in data["detail"]

    def test_enroll_course_creates_new(self):
        request = MagicMock()
        request.user = MagicMock()
        payload = EnrollmentIn(course_id=1)
        course = MagicMock()
        enrollment = MagicMock()
        with patch("courses.api.get_object_or_404", return_value=course):
            with patch("courses.api.Enrollment.objects.get_or_create", return_value=(enrollment, True)):
                result = enroll_course(request, payload)
                assert result["success"] is True
