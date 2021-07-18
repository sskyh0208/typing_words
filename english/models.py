from django.db import models
from django.utils import timezone
from accounts.models import Users


class WordBooks(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    publish = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'wordbooks'

    def __str__(self):
        return self.name

    
class Words(models.Model):
    wordbook = models.ForeignKey(
        WordBooks, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'words'

    def __str__(self):
        return self.name