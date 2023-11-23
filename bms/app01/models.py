from django.db import models


class User(models.Model):
    objects: models.query.QuerySet

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()
    sex = models.SmallIntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'

