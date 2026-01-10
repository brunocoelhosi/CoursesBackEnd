from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    workload = models.IntegerField(default=0)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title