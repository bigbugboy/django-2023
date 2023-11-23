from django.db import models


class Todo(models.Model):
    objects: models.manager.QuerySet

    STATUS_CHOICES = (
        (0, '未完成'),
        (1, '已完成'),
    )

    title = models.CharField(max_length=100)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateField(auto_now_add=True)
