from django.db import models
from django.db.models import Index


class CallCenter(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    ticket_id = models.IntegerField()
    ticket_description = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            Index(fields=['id']),
            Index(fields=['user_id']),
            Index(fields=['ticket_id']),
        ]
        ordering = ['id']

        def _str_(self):
            return self.nombre
