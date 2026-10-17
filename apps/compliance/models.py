from django.conf import settings
from django.db import models
class ComplianceTask(models.Model):
    STATUSES=[("pending","Pending"),("in_progress","In progress"),("review","In review"),("completed","Completed"),("blocked","Blocked")]
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="compliance_tasks")
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    due_date=models.DateField()
    status=models.CharField(max_length=15,choices=STATUSES,default="pending")
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="bizcfo_compliance_tasks")
    evidence_reference=models.CharField(max_length=255,blank=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["due_date"]
    def __str__(self): return self.title
