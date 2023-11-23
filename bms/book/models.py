from django.db import models


class Book(models.Model):
    objects: models.query.QuerySet

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    publish_date = models.DateField()
    publisher = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)

    class Meta:
        db_table = 'book'
