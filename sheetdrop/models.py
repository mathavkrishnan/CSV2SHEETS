from django.db import models

class CSV_FILES(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField()
