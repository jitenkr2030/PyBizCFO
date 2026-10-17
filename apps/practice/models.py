from django.conf import settings
from django.db import models
class WorkTask(models.Model):
    STATUS=[("todo","To do"),("doing","In progress"),("review","In review"),("done","Done")]
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="work_tasks")
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    due_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default="todo")
    created_at=models.DateTimeField(auto_now_add=True)
