from django.conf import settings
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=180)
    legal_name = models.CharField(max_length=220, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=3, default="INR")
    financial_year_start_month = models.PositiveSmallIntegerField(default=4)
    pan = models.CharField(max_length=20, blank=True)
    gstin = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Membership", related_name="bizcfo_organizations")
    def __str__(self): return self.name

class Membership(models.Model):
    ROLE_CHOICES = [(x,x.title()) for x in ["admin","owner","cfo","accountant","compliance","client_staff","auditor"]]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client_staff")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization","user"], name="uniq_org_member")]
    def __str__(self): return f"{self.user} — {self.organization} ({self.role})"
