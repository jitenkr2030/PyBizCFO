from django.conf import settings
from django.db import models
class AuditEvent(models.Model):
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    organization=models.ForeignKey("organizations.Organization",null=True,blank=True,on_delete=models.SET_NULL)
    event_type=models.CharField(max_length=100)
    object_ref=models.CharField(max_length=100,blank=True)
    details=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
