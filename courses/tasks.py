from celery import shared_task
from .models import Course
from services.openai_service import generate_course_image

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={"max_retries": 3})
def generate_course_image_task(self, course_id):
    course = Course.objects.get(id=course_id)

    image_url = generate_course_image(course.title, course.description)

    course.image_url = image_url
    course.save(update_fields=["image_url"])
