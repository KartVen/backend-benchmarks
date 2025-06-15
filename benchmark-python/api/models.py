from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    class Meta:
        db_table = "person"