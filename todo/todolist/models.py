from django.db import models


class TodoList(models.Model):
    objects: models.query.QuerySet

    title = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'todolist'
        ordering = ['-created_at', '-id']
