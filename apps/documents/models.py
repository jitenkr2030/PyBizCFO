from django.conf import settings
from django.db import models
from pathlib import Path
def private_upload_path(instance, filename):
    safe_name=Path(filename).name.replace("..","_")
    return f"org_{instance.organization_id}/documents/{safe_name}"
class Document(models.Model):
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="documents")
    title=models.CharField(max_length=180)
    file=models.FileField(upload_to=private_upload_path)
    uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=80,blank=True)
    is_confidential=models.BooleanField(default=True)
    def __str__(self): return self.title
