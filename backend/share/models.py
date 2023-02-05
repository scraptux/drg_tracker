import uuid
from django.db import models

class ShareData(models.Model):
    Code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JSON = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)