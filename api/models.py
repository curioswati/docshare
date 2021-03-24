from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Document(models.Model):
    doc_id = models.AutoField(primary_key=True, unique=True)
    doc = models.FileField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    editor = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=timezone.now)
    version = models.IntegerField()

    def __str__(self):
        return str(self.doc.name)
